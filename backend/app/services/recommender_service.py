"""
Rule-Based Recommendation Engine.
Implements FR-REC-01, FR-REC-02, FR-REC-03, and FR-REC-04.

Rule Overview:
1. FR-REC-01 (Category Match):
   Recommend products from the category currently discussed or explicitly queried.
2. FR-REC-02 (Budget Matching ±20%):
   When a budget $B is specified, filter and prioritize products where:
   (B * (1 - tolerance)) <= price <= (B * (1 + tolerance))
   Default tolerance is 20% (0.20) from config.py.
3. FR-REC-03 (Fallback / Cold-Start):
   If no category, product, or budget context exists, recommend top N featured/popular products
   (products with is_featured = 1).
"""

import json
from typing import List, Dict, Any, Optional
from ..config import RECOMMENDATION_CONFIG
from ..database import get_db_connection

class RecommenderService:
    @staticmethod
    def get_all_products() -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products ORDER BY id ASC")
        rows = cursor.fetchall()
        conn.close()

        products = []
        for r in rows:
            p = dict(r)
            if isinstance(p["specs"], str):
                p["specs"] = json.loads(p["specs"])
            p["is_featured"] = bool(p["is_featured"])
            products.append(p)
        return products

    @classmethod
    def get_featured_products(cls, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        FR-REC-03: When no prior context exists, return top N popular/featured products.
        """
        if limit is None:
            limit = RECOMMENDATION_CONFIG.get("default_featured_count", 4)

        all_products = cls.get_all_products()
        featured = [p for p in all_products if p.get("is_featured")]
        return featured[:limit]

    @classmethod
    def recommend(
        cls,
        category: Optional[str] = None,
        budget: Optional[float] = None,
        exclude_id: Optional[int] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Multi-rule recommendation pipeline:
        1. If category and budget are both provided:
           Matches category AND (budget ± 20%).
        2. If only budget is provided:
           Finds products across categories within (budget ± 20%).
        3. If only category is provided:
           Finds products in that category (featured first).
        4. If neither is provided:
           Falls back to FR-REC-03 (featured products).
        """
        if limit is None:
            limit = RECOMMENDATION_CONFIG.get("max_recommendations", 4)
        tolerance = RECOMMENDATION_CONFIG.get("budget_tolerance_percentage", 0.20)

        all_products = cls.get_all_products()
        candidates = all_products

        if exclude_id:
            candidates = [p for p in candidates if p["id"] != exclude_id]

        # Rule 1: Category Match (FR-REC-01)
        if category:
            cat_matches = [p for p in candidates if p["category"].lower() == category.lower()]
            if cat_matches:
                candidates = cat_matches

        # Rule 2: Budget Match (FR-REC-02) within ±20%
        if budget:
            min_price = budget * (1.0 - tolerance)
            max_price = budget * (1.0 + tolerance)

            # Strict budget match
            budget_matches = [p for p in candidates if min_price <= p["price"] <= max_price]

            # If no products fall strictly within ±20%, find closest products under or near budget
            if not budget_matches and candidates:
                budget_matches = sorted(candidates, key=lambda x: abs(x["price"] - budget))[:limit]

            if budget_matches:
                # Sort by how close they are to the desired budget, featured first
                budget_matches.sort(key=lambda p: (0 if p["is_featured"] else 1, abs(p["price"] - budget)))
                return budget_matches[:limit]

        # Rule 3: Category match fallback sorting (Featured first, then by popularity/id)
        if category and candidates:
            candidates.sort(key=lambda p: 0 if p["is_featured"] else 1)
            return candidates[:limit]

        # Rule 4: No prior context (FR-REC-03)
        return cls.get_featured_products(limit)

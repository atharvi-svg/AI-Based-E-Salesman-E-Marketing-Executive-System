"""
Lead scoring and classification service.
Implements FR-LEAD-01, FR-LEAD-02, FR-LEAD-03, FR-LEAD-04, and duplicate prevention.

Exact Scoring Points (from config.py):
- price_query: +5
- viewed_3_products: +5
- compare_query: +10
- purchase_intent: +20
- added_to_cart: +15

Classification Thresholds:
- Cold: 0 - 14
- Warm: 15 - 34
- Hot: 35+
"""

import json
from datetime import datetime
from typing import Dict, Any, Tuple, Optional, List
from ..config import LEAD_SCORING_POINTS, LEAD_THRESHOLDS
from ..database import get_db_connection

class LeadScoringService:
    @staticmethod
    def classify_score(score: int) -> str:
        """
        Classifies lead score into Cold, Warm, or Hot.
        """
        if score >= LEAD_THRESHOLDS["HOT_MIN"]:
            return "Hot"
        elif score >= LEAD_THRESHOLDS["WARM_MIN"]:
            return "Warm"
        else:
            return "Cold"

    @classmethod
    def get_or_create_lead(
        cls,
        session_id: str,
        name: Optional[str] = None,
        contact: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieves lead record for session, or creates a new one starting at score 0 (FR-LEAD-01, FR-CRM-01).
        """
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM leads WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if row:
            lead = dict(row)
            lead["scored_actions"] = json.loads(lead.get("scored_actions") or "[]")
            lead["viewed_products"] = json.loads(lead.get("viewed_products") or "[]")
            lead["is_converted"] = bool(lead["is_converted"])

            # Update contact info if newly provided
            if name and not lead.get("name"):
                cursor.execute("UPDATE leads SET name = ? WHERE id = ?", (name, lead["id"]))
                lead["name"] = name
            if contact and not lead.get("contact"):
                cursor.execute("UPDATE leads SET contact = ? WHERE id = ?", (contact, lead["id"]))
                lead["contact"] = contact
            conn.commit()
            conn.close()
            return lead

        # Create new lead
        initial_score = 0
        initial_status = "Cold"
        cursor.execute("""
        INSERT INTO leads (session_id, name, contact, score, status, created_at, last_interaction, is_converted, scored_actions, viewed_products)
        VALUES (?, ?, ?, ?, ?, ?, ?, 0, '[]', '[]')
        """, (session_id, name, contact, initial_score, initial_status, now_iso, now_iso))
        conn.commit()
        lead_id = cursor.lastrowid
        conn.close()

        return {
            "id": lead_id,
            "session_id": session_id,
            "name": name,
            "contact": contact,
            "score": initial_score,
            "status": initial_status,
            "created_at": now_iso,
            "last_interaction": now_iso,
            "is_converted": False,
            "scored_actions": [],
            "viewed_products": []
        }

    @classmethod
    def record_action(
        cls,
        session_id: str,
        action_key: str,
        product_id: Optional[int] = None
    ) -> Tuple[int, str, int, Optional[str]]:
        """
        Evaluates customer action and updates lead score if eligible.
        Prevents accidental repeated scoring for the same action per user requirements.

        Returns: (current_score, current_status, score_increment, reason)
        """
        lead = cls.get_or_create_lead(session_id)
        current_score = lead["score"]
        scored_actions = list(lead["scored_actions"])
        viewed_products = set(lead["viewed_products"])

        increment = 0
        reason = None
        now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 1. Product viewing check: track unique product views
        if product_id is not None and product_id not in viewed_products:
            viewed_products.add(product_id)
            if len(viewed_products) >= 3 and "viewed_3_products" not in scored_actions:
                points = LEAD_SCORING_POINTS.get("viewed_3_products", 5)
                increment += points
                scored_actions.append("viewed_3_products")
                reason = f"Viewed 3+ products (+{points})"

        # 2. Main action scoring with duplicate protection
        if action_key in LEAD_SCORING_POINTS:
            if action_key not in scored_actions:
                points = LEAD_SCORING_POINTS[action_key]
                increment += points
                scored_actions.append(action_key)
                action_labels = {
                    "price_query": "Asking about price",
                    "compare_query": "Asking for product comparison",
                    "purchase_intent": "Expressing purchase intent",
                    "added_to_cart": "Adding product to cart"
                }
                reason = f"{action_labels.get(action_key, action_key)} (+{points})"

        new_score = current_score + increment
        new_status = cls.classify_score(new_score)

        # Update in database (FR-LEAD-04, FR-CRM-03)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE leads
        SET score = ?, status = ?, scored_actions = ?, viewed_products = ?, last_interaction = ?
        WHERE session_id = ?
        """, (
            new_score,
            new_status,
            json.dumps(scored_actions),
            json.dumps(list(viewed_products)),
            now_iso,
            session_id
        ))
        conn.commit()
        conn.close()

        return new_score, new_status, increment, reason

    @classmethod
    def mark_converted(
        cls,
        session_id: str,
        customer_name: Optional[str] = None,
        customer_contact: Optional[str] = None
    ) -> bool:
        """
        Marks lead as converted upon simulated checkout completion (FR-PUR-03).
        """
        now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE leads
        SET is_converted = 1,
            name = COALESCE(?, name),
            contact = COALESCE(?, contact),
            last_interaction = ?
        WHERE session_id = ?
        """, (customer_name, customer_contact, now_iso, session_id))

        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        return rows_affected > 0

"""
Products API router.
"""

import json
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from ..database import get_db_connection
from ..models import Product
from ..services.recommender_service import RecommenderService
from ..services.chat_service import ChatService

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("", response_model=List[Product])
def get_products(
    category: Optional[str] = None,
    budget: Optional[float] = None,
    search: Optional[str] = None
):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM products WHERE 1=1"
    params = []

    if category and category.lower() != "all":
        query += " AND LOWER(category) = LOWER(?)"
        params.append(category)

    if budget:
        query += " AND price <= ?"
        params.append(budget)

    if search:
        query += " AND (LOWER(name) LIKE ? OR LOWER(description) LIKE ?)"
        like_str = f"%{search.lower()}%"
        params.extend([like_str, like_str])

    query += " ORDER BY is_featured DESC, price ASC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    products = []
    for r in rows:
        p = dict(r)
        p["specs"] = json.loads(p["specs"])
        p["is_featured"] = bool(p["is_featured"])
        products.append(Product(**p))

    return products

@router.get("/featured", response_model=List[Product])
def get_featured_products(limit: int = 4):
    products = RecommenderService.get_featured_products(limit)
    return [Product(**p) for p in products]

@router.get("/compare")
def compare_products(id1: int = Query(...), id2: int = Query(...)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id IN (?, ?)", (id1, id2))
    rows = cursor.fetchall()
    conn.close()

    if len(rows) < 2:
        raise HTTPException(status_code=404, detail="One or both products not found for comparison")

    prods = []
    for r in rows:
        p = dict(r)
        p["specs"] = json.loads(p["specs"])
        p["is_featured"] = bool(p["is_featured"])
        prods.append(p)

    p1 = prods[0] if prods[0]["id"] == id1 else prods[1]
    p2 = prods[1] if prods[0]["id"] == id1 else prods[0]

    return ChatService._generate_comparison(p1, p2)

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Product not found")

    p = dict(row)
    p["specs"] = json.loads(p["specs"])
    p["is_featured"] = bool(p["is_featured"])
    return Product(**p)

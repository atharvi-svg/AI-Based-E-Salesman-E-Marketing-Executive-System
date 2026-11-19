"""
Admin and CRM API router.
Implements FR-CRM-04 and Admin dashboard metrics.
"""

import json
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from ..database import get_db_connection
from ..models import AdminMetrics, LeadRecord, LeadDetailResponse, ChatLogItem

router = APIRouter(prefix="/api/admin", tags=["Admin & CRM"])

@router.get("/metrics", response_model=AdminMetrics)
def get_metrics():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM leads")
    total_leads = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM leads WHERE status = 'Hot'")
    hot_leads = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM leads WHERE status = 'Warm'")
    warm_leads = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM leads WHERE status = 'Cold'")
    cold_leads = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM leads WHERE is_converted = 1")
    total_conversions = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(total_price), 0.0) FROM orders")
    total_revenue = cursor.fetchone()[0]

    conn.close()

    conversion_rate = round((total_conversions / total_leads * 100), 1) if total_leads > 0 else 0.0

    return AdminMetrics(
        total_leads=total_leads,
        hot_leads=hot_leads,
        warm_leads=warm_leads,
        cold_leads=cold_leads,
        total_conversions=total_conversions,
        conversion_rate=conversion_rate,
        total_revenue=float(total_revenue)
    )

@router.get("/leads", response_model=List[LeadRecord])
def get_leads(
    status: Optional[str] = None,
    converted: Optional[bool] = None,
    sort_by: str = Query("score", regex="^(score|created_at|last_interaction)$"),
    order: str = Query("desc", regex="^(asc|desc)$")
):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM leads WHERE 1=1"
    params = []

    if status and status.lower() != "all":
        query += " AND LOWER(status) = LOWER(?)"
        params.append(status)

    if converted is not None:
        query += " AND is_converted = ?"
        params.append(1 if converted else 0)

    query += f" ORDER BY {sort_by} {order.upper()}"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    leads = []
    for r in rows:
        lead_dict = dict(r)
        lead_dict["scored_actions"] = json.loads(lead_dict.get("scored_actions") or "[]")
        lead_dict["is_converted"] = bool(lead_dict["is_converted"])
        leads.append(LeadRecord(**lead_dict))

    return leads

@router.get("/leads/{lead_id}", response_model=LeadDetailResponse)
def get_lead_details(lead_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Lead record
    cursor.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    lead_row = cursor.fetchone()
    if not lead_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Lead not found")

    lead_dict = dict(lead_row)
    lead_dict["scored_actions"] = json.loads(lead_dict.get("scored_actions") or "[]")
    lead_dict["is_converted"] = bool(lead_dict["is_converted"])
    session_id = lead_dict["session_id"]

    # 2. Chat logs
    cursor.execute("""
    SELECT id, sender, message, intent, extra_data, timestamp
    FROM chat_logs
    WHERE session_id = ? OR lead_id = ?
    ORDER BY id ASC
    """, (session_id, lead_id))
    chat_rows = cursor.fetchall()

    chat_logs = []
    for cr in chat_rows:
        item = dict(cr)
        if item.get("extra_data"):
            item["extra_data"] = json.loads(item["extra_data"])
        chat_logs.append(ChatLogItem(**item))

    # 3. Orders
    cursor.execute("""
    SELECT id, total_price, product_ids, status, created_at
    FROM orders
    WHERE lead_id = ? OR session_id = ?
    ORDER BY id DESC
    """, (lead_id, session_id))
    order_rows = cursor.fetchall()

    orders = []
    for o in order_rows:
        od = dict(o)
        od["product_ids"] = json.loads(od["product_ids"])
        orders.append(od)

    conn.close()

    return LeadDetailResponse(
        lead=LeadRecord(**lead_dict),
        chat_logs=chat_logs,
        orders=orders
    )

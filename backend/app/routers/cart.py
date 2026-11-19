"""
Cart and Simulated Checkout API router.
Implements FR-PUR-01, FR-PUR-02, FR-PUR-03, and lead conversion.
"""

import json
from datetime import datetime
from fastapi import APIRouter, HTTPException
from ..models import AddToCartRequest, CheckoutRequest, CheckoutResponse
from ..services.lead_scoring_service import LeadScoringService
from ..database import get_db_connection

router = APIRouter(prefix="/api/cart", tags=["Cart & Checkout"])

@router.post("/add")
def add_to_cart(payload: AddToCartRequest):
    """
    Handles adding product to cart (FR-PUR-01).
    Scores +15 points for adding to cart (FR-LEAD-02) with duplicate prevention.
    """
    new_score, new_status, increment, reason = LeadScoringService.record_action(
        session_id=payload.session_id,
        action_key="added_to_cart",
        product_id=payload.product_id
    )

    return {
        "success": True,
        "product_id": payload.product_id,
        "quantity": payload.quantity,
        "lead_score": new_score,
        "lead_status": new_status,
        "score_increment": increment,
        "scored_reason": reason
    }

@router.post("/checkout", response_model=CheckoutResponse)
def simulated_checkout(payload: CheckoutRequest):
    """
    Completes simulated checkout (FR-PUR-02, FR-PUR-03).
    - Creates order record in database.
    - Marks customer lead as converted in CRM.
    """
    if not payload.items:
        raise HTTPException(status_code=400, detail="Cannot checkout with an empty cart.")

    lead = LeadScoringService.get_or_create_lead(
        session_id=payload.session_id,
        name=payload.customer_name,
        contact=payload.customer_contact
    )
    lead_id = lead["id"]

    now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    product_summary = [
        {"product_id": i.product_id, "name": i.name, "quantity": i.quantity, "price": i.price}
        for i in payload.items
    ]

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Insert order record
    cursor.execute("""
    INSERT INTO orders (lead_id, session_id, customer_name, customer_contact, product_ids, total_price, status, created_at)
    VALUES (?, ?, ?, ?, ?, ?, 'Completed', ?)
    """, (
        lead_id,
        payload.session_id,
        payload.customer_name,
        payload.customer_contact,
        json.dumps(product_summary),
        payload.total_price,
        now_iso
    ))
    order_id = cursor.lastrowid

    # 2. Mark lead as converted (FR-PUR-03)
    cursor.execute("""
    UPDATE leads
    SET is_converted = 1,
        name = ?,
        contact = ?,
        last_interaction = ?
    WHERE session_id = ?
    """, (
        payload.customer_name,
        payload.customer_contact,
        now_iso,
        payload.session_id
    ))

    # 3. Log simulated checkout completion in chat logs
    checkout_log_msg = (
        f"✅ Order #{order_id} Confirmed! Total: ${payload.total_price:.2f}. "
        f"Recipient: {payload.customer_name} ({payload.customer_contact}). "
        f"Lead successfully converted."
    )
    cursor.execute("""
    INSERT INTO chat_logs (lead_id, session_id, sender, message, intent, extra_data, timestamp)
    VALUES (?, ?, 'bot', ?, 'simulated_checkout', ?, ?)
    """, (
        lead_id,
        payload.session_id,
        checkout_log_msg,
        json.dumps({"order_id": order_id, "total": payload.total_price}),
        now_iso
    ))

    conn.commit()
    conn.close()

    return CheckoutResponse(
        order_id=order_id,
        lead_id=lead_id,
        session_id=payload.session_id,
        total_price=payload.total_price,
        status="Completed",
        message="Simulated checkout completed successfully. Lead marked as converted in CRM."
    )

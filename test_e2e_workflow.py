"""
End-to-End System Integration Test for AI-Salesman.
Directly executes the required 10-step academic review workflow from Section 6 of prompt:

1. Customer opens the application (session initialized).
2. Customer asks for a laptop under a specified budget ($1000).
3. Assistant displays matching products.
4. Customer asks for a product comparison.
5. Lead score increases correctly (transparent scoring & classification).
6. Customer adds a product to cart (lead score increases +15).
7. Customer completes simulated checkout.
8. Lead is marked as converted.
9. Admin opens the dashboard (fetches metrics and leads list).
10. Admin inspects the customer: sees lead score, classification, conversation history, and conversion status.
"""

import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from app.database import init_db, get_db_connection
from app.seed_data import seed_products
from app.routers import products, chat, cart, admin
from app.models import (
    ChatMessageRequest, AddToCartRequest, CheckoutRequest, CartItem
)

def run_e2e_workflow():
    print("=" * 70)
    print("STARTING E2E INTEGRATION TEST: 10-STEP ACADEMIC REVIEW WORKFLOW")
    print("=" * 70)

    # Reset DB & Seed
    init_db()
    seed_products(force=True)

    session_id = "evaluator_e2e_review_session_001"
    customer_name = "Arun Kadli (Evaluator)"
    customer_contact = "arun.review@codeconnect.edu"

    # Step 1: Customer opens the application
    print("\n--- STEP 1: Customer opens application & initializes session ---")
    catalog = products.get_products()
    assert len(catalog) >= 20
    print(f"✅ Catalog loaded successfully. Available products: {len(catalog)}")

    # Step 2 & 3: Customer asks for a laptop under a specified budget ($1000)
    print("\n--- STEP 2 & 3: Customer asks for laptops under $1000 ---")
    req_budget = ChatMessageRequest(
        session_id=session_id,
        message="Show me laptops under $1000"
    )
    res_budget = chat.post_chat_message(req_budget)
    assert res_budget.intent == "recommendation_request"
    assert res_budget.products is not None and len(res_budget.products) > 0
    print(f"✅ Intent detected: '{res_budget.intent}'")
    print(f"✅ Assistant response: {res_budget.reply[:90]}...")
    print(f"✅ Matching products returned ({len(res_budget.products)} items):")
    for p in res_budget.products:
        print(f"   • {p.name} - ${p.price:.2f} ({p.stock_status})")

    # Step 4 & 5: Customer asks for product comparison
    print("\n--- STEP 4 & 5: Customer asks for comparison & lead score increases ---")
    req_compare = ChatMessageRequest(
        session_id=session_id,
        message="Can you compare Apple MacBook Air M2 and Asus ZenBook 14?"
    )
    res_compare = chat.post_chat_message(req_compare)
    assert res_compare.intent == "compare_query"
    assert res_compare.comparison is not None
    assert res_compare.lead_score == 10  # +10 for comparison
    assert res_compare.lead_status == "Cold"  # 10 is Cold (0-14)
    print(f"✅ Intent detected: '{res_compare.intent}'")
    print(f"✅ Comparison generated between {res_compare.comparison['product_a']['name']} and {res_compare.comparison['product_b']['name']}")
    print(f"✅ Lead Score increment: +{res_compare.score_increment} ({res_compare.scored_reason})")
    print(f"✅ Current Lead Score: {res_compare.lead_score} (Status: {res_compare.lead_status})")

    # Asking price to test price_query scoring (+5 -> score 15, Warm!)
    print("\n--- Customer asks for price of MacBook Air M2 (+5 pts) ---")
    req_price = ChatMessageRequest(
        session_id=session_id,
        message="What is the price of Apple MacBook Air M2?"
    )
    res_price = chat.post_chat_message(req_price)
    assert res_price.lead_score == 15
    assert res_price.lead_status == "Warm"  # 15-34 is Warm
    print(f"✅ Lead Score increment: +{res_price.score_increment} ({res_price.scored_reason})")
    print(f"✅ Lead Score updated: {res_price.lead_score} (Status: {res_price.lead_status})")

    # Step 6: Customer adds product to cart (+15 pts -> score 30, Warm!)
    print("\n--- STEP 6: Customer adds product to cart ---")
    req_add = AddToCartRequest(
        session_id=session_id,
        product_id=1,
        quantity=1
    )
    res_add = cart.add_to_cart(req_add)
    assert res_add["lead_score"] == 30
    assert res_add["lead_status"] == "Warm"
    print(f"✅ Item added to cart. Lead Score increment: +{res_add['score_increment']} ({res_add['scored_reason']})")
    print(f"✅ Current Lead Score: {res_add['lead_score']} (Status: {res_add['lead_status']})")

    # Customer expresses purchase intent (+20 pts -> score 50, Hot!)
    print("\n--- Customer expresses purchase intent (+20 pts -> Hot!) ---")
    req_intent = ChatMessageRequest(
        session_id=session_id,
        message="I want to purchase the MacBook Air right now"
    )
    res_intent = chat.post_chat_message(req_intent)
    assert res_intent.lead_score == 50
    assert res_intent.lead_status == "Hot"  # 35+ is Hot!
    print(f"✅ Lead Score increment: +{res_intent.score_increment} ({res_intent.scored_reason})")
    print(f"✅ Current Lead Score: {res_intent.lead_score} (Status: {res_intent.lead_status})")

    # Step 7 & 8: Customer completes simulated checkout -> Lead marked as converted
    print("\n--- STEP 7 & 8: Customer completes simulated checkout & marks converted ---")
    req_checkout = CheckoutRequest(
        session_id=session_id,
        customer_name=customer_name,
        customer_contact=customer_contact,
        items=[
            CartItem(
                product_id=1,
                name="Apple MacBook Air M2",
                price=999.00,
                quantity=1
            )
        ],
        total_price=999.00
    )
    res_checkout = cart.simulated_checkout(req_checkout)
    assert res_checkout.status == "Completed"
    print(f"✅ Simulated Checkout completed! Order ID: #{res_checkout.order_id}")
    print(f"✅ Message: {res_checkout.message}")

    # Step 9: Admin opens dashboard & fetches metrics and leads
    print("\n--- STEP 9: Admin opens dashboard ---")
    metrics = admin.get_metrics()
    print(f"✅ Admin Metrics Loaded:")
    print(f"   • Total Leads: {metrics.total_leads}")
    print(f"   • Hot Leads: {metrics.hot_leads}")
    print(f"   • Warm Leads: {metrics.warm_leads}")
    print(f"   • Cold Leads: {metrics.cold_leads}")
    print(f"   • Conversions: {metrics.total_conversions} ({metrics.conversion_rate}%)")
    print(f"   • Total Revenue: ${metrics.total_revenue:.2f}")

    leads_list = admin.get_leads(sort_by="score", order="desc")
    assert len(leads_list) > 0
    print(f"✅ Leads list loaded: {len(leads_list)} leads displayed.")

    # Step 10: Admin inspects the customer in CRM
    print("\n--- STEP 10: Admin sees customer details, score, classification, conversation history, and conversion status ---")
    matched_lead = next((l for l in leads_list if l.session_id == session_id), None)
    assert matched_lead is not None
    assert matched_lead.score == 50
    assert matched_lead.status == "Hot"
    assert matched_lead.is_converted is True
    assert matched_lead.name == customer_name
    assert matched_lead.contact == customer_contact

    details = admin.get_lead_details(matched_lead.id)
    print(f"✅ Lead Details Inspected:")
    print(f"   • Customer Name: {details.lead.name}")
    print(f"   • Contact: {details.lead.contact}")
    print(f"   • Session ID: {details.lead.session_id}")
    print(f"   • Score: {details.lead.score} ({details.lead.status})")
    print(f"   • Is Converted: {details.lead.is_converted}")
    print(f"   • Scored Actions: {details.lead.scored_actions}")
    print(f"   • Simulated Orders: {len(details.orders)}")
    print(f"   • Total Chat Messages in Transcript: {len(details.chat_logs)}")

    print("\n   Full Chat Transcript for this Lead:")
    for log in details.chat_logs:
        intent_str = f" [{log.intent}]" if log.intent else ""
        print(f"     [{log.timestamp}] {log.sender.upper()}{intent_str}: {log.message[:60]}...")

    print("\n" + "=" * 70)
    print("🎉 ALL 10 STEPS OF THE ACADEMIC REVIEW WORKFLOW PASSED WITH 100% SUCCESS!")
    print("=" * 70)

if __name__ == "__main__":
    run_e2e_workflow()

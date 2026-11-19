"""
Core Chat Service managing conversation context, intent dispatching,
product responses, lead scoring triggers, and CRM logging.
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

from .intent_service import IntentService
from .recommender_service import RecommenderService
from .lead_scoring_service import LeadScoringService
from ..database import get_db_connection

# In-memory session context cache to remember active product, category, and preferences (FR-CHAT-03)
SESSION_CONTEXT_CACHE: Dict[str, Dict[str, Any]] = {}

class ChatService:
    @classmethod
    def get_session_context(cls, session_id: str) -> Dict[str, Any]:
        if session_id not in SESSION_CONTEXT_CACHE:
            SESSION_CONTEXT_CACHE[session_id] = {
                "last_product_id": None,
                "last_category": None,
                "preferred_budget": None,
                "last_intent": None
            }
        return SESSION_CONTEXT_CACHE[session_id]

    @classmethod
    def log_message(
        cls,
        session_id: str,
        lead_id: int,
        sender: str,
        message: str,
        intent: Optional[str] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ):
        """
        Logs chat message to database (FR-CRM-02).
        """
        now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO chat_logs (lead_id, session_id, sender, message, intent, extra_data, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            lead_id,
            session_id,
            sender,
            message,
            intent,
            json.dumps(extra_data) if extra_data else None,
            now_iso
        ))
        conn.commit()
        conn.close()

    @classmethod
    def process_message(
        cls,
        session_id: str,
        user_message: str,
        user_name: Optional[str] = None,
        user_contact: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Main chat pipeline:
        1. Initialize/Retrieve Lead
        2. Detect Intent & Entities
        3. Dispatch to Domain Handlers
        4. Apply Lead Scoring Rules
        5. Persist Chat Logs in CRM
        6. Return Structured Response
        """
        lead = LeadScoringService.get_or_create_lead(session_id, user_name, user_contact)
        lead_id = lead["id"]
        ctx = cls.get_session_context(session_id)

        # Log incoming user message
        cls.log_message(session_id, lead_id, "customer", user_message)

        # Detect intent and extract entities
        intent, entities = IntentService.detect_intent(user_message)
        ctx["last_intent"] = intent

        all_products = RecommenderService.get_all_products()
        matched_products = IntentService.extract_product_candidates(user_message, all_products)

        # Update context if new category or budget specified
        if "category" in entities:
            ctx["last_category"] = entities["category"]
        if "budget" in entities:
            ctx["preferred_budget"] = entities["budget"]
        if matched_products:
            ctx["last_product_id"] = matched_products[0]["id"]
            ctx["last_category"] = matched_products[0]["category"]

        # Track product views in lead scoring (e.g. viewed 3+ products)
        for p in matched_products:
            LeadScoringService.record_action(session_id, "view_product", product_id=p["id"])

        # Dispatch based on intent
        reply = ""
        products_payload: Optional[List[Dict[str, Any]]] = None
        comparison_payload: Optional[Dict[str, Any]] = None
        suggested_prompts: List[str] = []
        action_key_to_score: Optional[str] = None

        # ----------------------------------------------------------------------
        # 1. COMPARE QUERY (FR-PROD-02, FR-LEAD-02: +10)
        # ----------------------------------------------------------------------
        if intent == "compare_query":
            action_key_to_score = "compare_query"
            if len(matched_products) >= 2:
                p1, p2 = matched_products[0], matched_products[1]
                comparison_payload = cls._generate_comparison(p1, p2)
                reply = (
                    f"Here is a side-by-side comparison between **{p1['name']}** and **{p2['name']}**:\n\n"
                    f"• **{p1['name']}**: ${p1['price']:.2f} ({p1['stock_status']})\n"
                    f"• **{p2['name']}**: ${p2['price']:.2f} ({p2['stock_status']})\n\n"
                    f"Check out the detailed specs comparison below. Would you like to add either of these to your cart?"
                )
                products_payload = [p1, p2]
                suggested_prompts = [
                    f"Add {p1['name']} to cart",
                    f"Add {p2['name']} to cart",
                    f"Show more in {p1['category']}"
                ]
            elif len(matched_products) == 1:
                p1 = matched_products[0]
                # Compare with a similar product in the same category
                similars = [p for p in all_products if p["category"] == p1["category"] and p["id"] != p1["id"]]
                if similars:
                    p2 = similars[0]
                    comparison_payload = cls._generate_comparison(p1, p2)
                    reply = (
                        f"You mentioned **{p1['name']}**. I've compared it against the popular alternative **{p2['name']}**:\n\n"
                        f"• **{p1['name']}**: ${p1['price']:.2f}\n"
                        f"• **{p2['name']}**: ${p2['price']:.2f}\n\n"
                        f"Review the key differences below! Which one suits your needs better?"
                    )
                    products_payload = [p1, p2]
                    suggested_prompts = [
                        f"Add {p1['name']} to cart",
                        f"Add {p2['name']} to cart",
                        f"What are the offers on {p1['name']}?"
                    ]
                else:
                    reply = f"I found **{p1['name']}** (${p1['price']:.2f}). Which other product would you like to compare it with?"
                    products_payload = [p1]
                    suggested_prompts = ["Compare with Dell XPS 15", "Compare with Asus ZenBook 14"]
            else:
                # Default comparison between top 2 laptops or featured products
                laptops = [p for p in all_products if p["category"] == "Laptops"]
                if len(laptops) >= 2:
                    p1, p2 = laptops[0], laptops[2]  # MacBook Air vs ZenBook
                    comparison_payload = cls._generate_comparison(p1, p2)
                    reply = (
                        f"Here is our most popular comparison: **{p1['name']}** vs **{p2['name']}**!\n\n"
                        f"Take a look at how they stack up in price and specs:"
                    )
                    products_payload = [p1, p2]
                    suggested_prompts = [
                        f"Buy {p1['name']}",
                        f"Buy {p2['name']}",
                        "Show laptops under $1000"
                    ]

        # ----------------------------------------------------------------------
        # 2. PRICE QUERY (FR-PROD-01, FR-LEAD-02: +5)
        # ----------------------------------------------------------------------
        elif intent == "price_query":
            action_key_to_score = "price_query"
            target_product = matched_products[0] if matched_products else cls._find_product_by_id(ctx.get("last_product_id"), all_products)

            if target_product:
                offer_text = f" 🔥 **Special Offer**: {target_product['offer_flag']}" if target_product.get("offer_flag") else ""
                reply = (
                    f"The price for **{target_product['name']}** is **${target_product['price']:.2f}**.\n"
                    f"• Status: **{target_product['stock_status']}**\n"
                    f"• Category: {target_product['category']}\n"
                    f"{offer_text}\n\n"
                    f"Would you like to review its technical specifications or add it to your cart?"
                )
                products_payload = [target_product]
                suggested_prompts = [
                    f"Specs of {target_product['name']}",
                    f"Add {target_product['name']} to cart",
                    f"Compare {target_product['name']} with another model"
                ]
            else:
                # General price inquiry
                featured = RecommenderService.get_featured_products(3)
                reply = "Here are our current prices for top featured items across the store. Which one would you like details on?"
                products_payload = featured
                suggested_prompts = [f"Price of {p['name']}" for p in featured]

        # ----------------------------------------------------------------------
        # 3. SPECIFICATIONS QUERY (FR-PROD-01)
        # ----------------------------------------------------------------------
        elif intent == "spec_query":
            target_product = matched_products[0] if matched_products else cls._find_product_by_id(ctx.get("last_product_id"), all_products)
            if target_product:
                specs_formatted = "\n".join([f"• **{k.replace('_', ' ').capitalize()}**: {v}" for k, v in target_product["specs"].items()])
                offer_text = f"\n• **Special Deal**: {target_product['offer_flag']}" if target_product.get("offer_flag") else ""
                reply = (
                    f"Here are the complete specifications for **{target_product['name']}**:\n\n"
                    f"{specs_formatted}\n"
                    f"• **Price**: ${target_product['price']:.2f}\n"
                    f"• **Availability**: {target_product['stock_status']}"
                    f"{offer_text}\n\n"
                    f"Ready to get this unit or want to compare it with another model?"
                )
                products_payload = [target_product]
                suggested_prompts = [
                    f"Add {target_product['name']} to cart",
                    f"Compare {target_product['name']} with other options",
                    f"Show similar {target_product['category']}"
                ]
            else:
                reply = "Which specific product would you like to see specifications for? We have top Laptops, Smartphones, Audio gear, and Smartwatches."
                products_payload = RecommenderService.get_featured_products(3)
                suggested_prompts = ["Specs for MacBook Air M2", "Specs for Galaxy S24 Ultra", "Specs for Sony WH-1000XM5"]

        # ----------------------------------------------------------------------
        # 4. OFFER / DISCOUNT QUERY (FR-PROD-03)
        # ----------------------------------------------------------------------
        elif intent == "offer_query":
            # List items with active offers
            items_with_offers = [p for p in all_products if p.get("offer_flag")]
            if matched_products and matched_products[0].get("offer_flag"):
                p = matched_products[0]
                reply = (
                    f"Yes! We currently have a special promotion on **{p['name']}**:\n\n"
                    f"🎉 **{p['offer_flag']}**\n"
                    f"Regular Price: ${p['price']:.2f} | Status: {p['stock_status']}\n\n"
                    f"Would you like me to add this deal to your cart?"
                )
                products_payload = [p]
            else:
                reply = "Here are today's top deals and limited-time discounts currently active in our store:"
                products_payload = items_with_offers[:4]

            suggested_prompts = [
                "Show laptops on offer",
                "Apply student discount",
                "Recommend best budget picks"
            ]

        # ----------------------------------------------------------------------
        # 5. RECOMMENDATION REQUEST (FR-REC-01, FR-REC-02, FR-REC-03)
        # ----------------------------------------------------------------------
        elif intent == "recommendation_request":
            budget = entities.get("budget") or ctx.get("preferred_budget")
            category = entities.get("category") or ctx.get("last_category")

            recommendations = RecommenderService.recommend(category=category, budget=budget)
            products_payload = recommendations

            if category and budget:
                reply = (
                    f"Based on your budget of **${budget:,.2f}** (evaluating within ±20%), here are our best recommended **{category}**:\n\n"
                    f"These options deliver outstanding performance and value in your target price range."
                )
            elif budget:
                reply = (
                    f"Here are top-tier recommendations fitting comfortably around your **${budget:,.2f}** budget (±20% range):\n\n"
                    f"Feel free to ask for detailed specs or a side-by-side comparison!"
                )
            elif category:
                reply = (
                    f"Here are our most popular and highest-rated **{category}** available right now:"
                )
            else:
                reply = (
                    "Here are our top featured and bestselling electronics right now! Let me know your preferred category or budget to personalize these:"
                )

            suggested_prompts = [
                f"Compare top 2 {category or 'options'}",
                f"Show {category or 'laptops'} under $1000",
                "Any current discounts?"
            ]

        # ----------------------------------------------------------------------
        # 6. PURCHASE INTENT (FR-PUR-01, FR-LEAD-02: +20)
        # ----------------------------------------------------------------------
        elif intent == "purchase_intent":
            action_key_to_score = "purchase_intent"
            target_product = matched_products[0] if matched_products else cls._find_product_by_id(ctx.get("last_product_id"), all_products)

            if target_product:
                reply = (
                    f"Fantastic choice! **{target_product['name']}** (${target_product['price']:.2f}) is in stock and ready to ship.\n\n"
                    f"You can add it directly to your cart right now using the button below, or proceed straight to checkout for simulated instant order placement!"
                )
                products_payload = [target_product]
                suggested_prompts = [
                    f"Add {target_product['name']} to cart",
                    "Proceed to Checkout",
                    "Check warranty details"
                ]
            else:
                reply = (
                    "Excellent! We are ready to assist with your order. You can add any item to your cart and complete our simulated checkout instantly with zero payment required.\n\n"
                    "Which product would you like to purchase today?"
                )
                products_payload = RecommenderService.get_featured_products(3)
                suggested_prompts = [
                    "Buy Apple MacBook Air M2",
                    "Buy Sony WH-1000XM5",
                    "View my cart"
                ]

        # ----------------------------------------------------------------------
        # 7. GENERAL / GREETING (FR-CHAT-04)
        # ----------------------------------------------------------------------
        elif intent == "general/greeting":
            reply = (
                "👋 Hello and welcome to AI-Salesman! I am your AI Virtual Sales & Marketing Executive.\n\n"
                "I can help you:\n"
                "• 🔍 **Find products** by category or budget (e.g. *'Laptops under $1000'*)\n"
                "• ⚖️ **Compare models** side-by-side (e.g. *'Compare MacBook vs ZenBook'*)\n"
                "• 🏷️ **Check prices, specifications, and special offers**\n"
                "• 🛒 **Add items to your cart** and complete instant simulated checkout\n\n"
                "What kind of tech are you looking for today?"
            )
            products_payload = RecommenderService.get_featured_products(3)
            suggested_prompts = [
                "Laptops under $1000",
                "Compare MacBook Air M2 vs Asus ZenBook 14",
                "Show active discounts & deals",
                "Top smartphones"
            ]

        # ----------------------------------------------------------------------
        # 8. UNKNOWN (FR-CHAT-05: Clarifying question, graceful handling)
        # ----------------------------------------------------------------------
        else:
            intent = "unknown"
            reply = (
                "I'm not sure I understood your query completely. Could you please clarify what you're looking for?\n\n"
                "For example, you can tell me a budget (e.g. *'laptops under $800'*), ask for a spec comparison (e.g. *'compare iPhone 15 Pro and Galaxy S24 Ultra'*), or ask about current deals."
            )
            suggested_prompts = [
                "Show laptops under $1000",
                "Compare top headphones",
                "What deals do you have today?"
            ]

        # Apply Lead Scoring Trigger if applicable
        current_score = lead["score"]
        current_status = lead["status"]
        increment = 0
        reason = None

        if action_key_to_score:
            current_score, current_status, increment, reason = LeadScoringService.record_action(
                session_id=session_id,
                action_key=action_key_to_score
            )
        else:
            # Refresh lead data in case views updated it
            refreshed = LeadScoringService.get_or_create_lead(session_id)
            current_score = refreshed["score"]
            current_status = refreshed["status"]

        # Log bot reply
        log_extra = {}
        if products_payload:
            log_extra["product_ids"] = [p["id"] for p in products_payload]
        if comparison_payload:
            log_extra["comparison"] = True

        cls.log_message(
            session_id=session_id,
            lead_id=lead_id,
            sender="bot",
            message=reply,
            intent=intent,
            extra_data=log_extra
        )

        return {
            "session_id": session_id,
            "reply": reply,
            "intent": intent,
            "lead_score": current_score,
            "lead_status": current_status,
            "score_increment": increment,
            "scored_reason": reason,
            "products": products_payload,
            "comparison": comparison_payload,
            "suggested_prompts": suggested_prompts
        }

    @staticmethod
    def _find_product_by_id(product_id: Optional[int], products: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if not product_id:
            return None
        for p in products:
            if p["id"] == product_id:
                return p
        return None

    @staticmethod
    def _generate_comparison(p1: Dict[str, Any], p2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates side-by-side comparison structure between two products (FR-PROD-02).
        """
        all_spec_keys = set(p1["specs"].keys()).union(set(p2["specs"].keys()))
        spec_matrix = []
        for key in sorted(all_spec_keys):
            val1 = p1["specs"].get(key, "N/A")
            val2 = p2["specs"].get(key, "N/A")
            spec_matrix.append({
                "feature": key.replace("_", " ").capitalize(),
                "product_a": val1,
                "product_b": val2,
                "different": val1 != val2
            })

        return {
            "product_a": {
                "id": p1["id"],
                "name": p1["name"],
                "price": p1["price"],
                "category": p1["category"],
                "stock_status": p1["stock_status"],
                "offer_flag": p1.get("offer_flag"),
                "image_url": p1.get("image_url")
            },
            "product_b": {
                "id": p2["id"],
                "name": p2["name"],
                "price": p2["price"],
                "category": p2["category"],
                "stock_status": p2["stock_status"],
                "offer_flag": p2.get("offer_flag"),
                "image_url": p2.get("image_url")
            },
            "price_difference": round(abs(p1["price"] - p2["price"]), 2),
            "cheaper_product_id": p1["id"] if p1["price"] <= p2["price"] else p2["id"],
            "spec_matrix": spec_matrix
        }

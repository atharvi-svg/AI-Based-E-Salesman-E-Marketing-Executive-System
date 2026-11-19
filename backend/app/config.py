"""
Configuration module for AI-Salesman system.
Per NFR-MAIN-01, lead scoring rules, thresholds, and recommendation parameters
are consolidated here so they can be easily modified without altering core application logic.
"""

# ==============================================================================
# LEAD SCORING CONFIGURATION (FR-LEAD-01, FR-LEAD-02, FR-LEAD-03)
# ==============================================================================

LEAD_SCORING_POINTS = {
    "price_query": 5,        # Asking about price (+5)
    "viewed_3_products": 5,  # Viewing 3 or more products (+5)
    "compare_query": 10,     # Asking for a comparison (+10)
    "purchase_intent": 20,   # Mentioning intent to buy (+20)
    "added_to_cart": 15,     # Adding a product to cart (+15)
}

# Lead Classification Thresholds (FR-LEAD-03)
# Cold: 0 - 14
# Warm: 15 - 34
# Hot: 35+
LEAD_THRESHOLDS = {
    "COLD_MAX": 14,
    "WARM_MIN": 15,
    "WARM_MAX": 34,
    "HOT_MIN": 35,
}

# ==============================================================================
# RECOMMENDATION ENGINE CONFIGURATION (FR-REC-01, FR-REC-02, FR-REC-03)
# ==============================================================================

RECOMMENDATION_CONFIG = {
    "budget_tolerance_percentage": 0.20,  # ±20% of budget mentioned (FR-REC-02)
    "default_featured_count": 4,          # Top N popular products if no prior context (FR-REC-03)
    "max_recommendations": 4,
}

# Supported intents as defined in FR-CHAT-04:
SUPPORTED_INTENTS = [
    "price_query",
    "spec_query",
    "compare_query",
    "offer_query",
    "recommendation_request",
    "purchase_intent",
    "general/greeting",
    "unknown",
]

# Database Path
DB_PATH = "backend/data/ai_salesman.db"

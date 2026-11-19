# AI-Based E-Salesman & E-Marketing Executive System

**Course:** UE24CS341A – Software Engineering  
**Project Type:** Jackfruit SE Mini-Project  
**Team Name:** Code Connect (Project ID: 15)  
**Team Members:** Atharvi (Repo Admin), Chandana (Requirements Analyst), Harika (Documentation Lead), Arun (Reviewer)  
**Document Reference:** [SRS.pdf](SRS.pdf) (Version 2.0)



## 1. Project Overview

**AI-Salesman** is an integrated AI-driven virtual sales and marketing assistant tailored for modern e-commerce. It enables shoppers to interact in real-time with an AI sales executive to discover tech products, query prices and detailed specifications, compare products side-by-side, receive recommendations based on budget and category, add items to a cart, and execute an instant simulated checkout.

Concurrently, a built-in **Internal CRM & Admin Dashboard** provides sales and marketing teams with real-time visibility into lead generation, transparent behavioral lead scoring (+points for price inquiries, product comparisons, purchase intent, cart actions), dynamic Cold/Warm/Hot classifications, complete chat transcripts, and conversion analytics.

The application also supports context-aware chat, natural-language product discovery, product comparisons, rule-based recommendations, a simulated cart and checkout, and lead and sales analytics.

## Features

- Text chat with intent detection for product, price, specification, comparison, offer, and purchase questions
- Product discovery by search, category, and budget
- Context-aware recommendations using product category and budget
- Lead scoring and Cold/Warm/Hot classification, with chat transcripts in the built-in CRM
- Product comparison, simulated cart and checkout, and an admin dashboard


## 2. Technology Stack

- **Frontend:** React.js 18 + Tailwind CSS + Lucide Icons (powered by Vite)
- **Backend:** Python 3 + FastAPI + Uvicorn (REST API)
- **Database:** SQLite (persisting `products`, `leads`, `chat_logs`, `orders`)
- **AI / NLP Logic:** Rule-based intent detection engine with transparent regex patterns and configurable thresholds (`backend/app/config.py`)

## Project Structure

```text
backend/             FastAPI application, services, and tests
frontend/            React/Vite application and npm lockfile
SRS.pdf              Software Requirements Specification
Software_Architecture_Person4.docx
                     Software architecture document
use_case_diagram.png Use-case diagram
test_e2e_workflow.py End-to-end workflow test
```

See [SRS.pdf](SRS.pdf) for requirements and project scope, [Software_Architecture_Person4.docx](Software_Architecture_Person4.docx) for the software architecture, and [use_case_diagram.png](use_case_diagram.png) for the use-case diagram.


## 3. SRS Requirements Compliance Matrix

| SRS Req ID | Module | Feature Description | Status |
| :--- | :--- | :--- | :--- |
| **FR-CHAT-01** | Chat Interface | Text chat window on website for customer messaging | ✅ Fully Implemented |
| **FR-CHAT-02** | Chat Interface | Bot replies displayed in real-time in the same window | ✅ Fully Implemented |
| **FR-CHAT-03** | Chat Interface | Session context remembered across turns (active product, category, budget) | ✅ Fully Implemented |
| **FR-CHAT-04** | Chat Interface | Intent detection for 8 defined types (`price_query`, `spec_query`, `compare_query`, `offer_query`, `recommendation_request`, `purchase_intent`, `general/greeting`, `unknown`) | ✅ Fully Implemented |
| **FR-CHAT-05** | Chat Interface | Graceful clarification when intent is `unknown` | ✅ Fully Implemented |
| **FR-PROD-01** | Product Management | Retrieval of price, specs, stock status, and descriptions from DB | ✅ Fully Implemented |
| **FR-PROD-02** | Product Management | Side-by-side comparison of two named products (price & key specs) | ✅ Fully Implemented |
| **FR-PROD-03** | Product Management | Automatic highlighting of active product discount/offer flags | ✅ Fully Implemented |
| **FR-REC-01** | Recommender | Same-category recommendations based on context | ✅ Fully Implemented |
| **FR-REC-02** | Recommender | Recommendation matching within ±20% of customer budget | ✅ Fully Implemented |
| **FR-REC-03** | Recommender | Fallback to top N popular/featured products when no context exists | ✅ Fully Implemented |
| **FR-REC-04** | Recommender | Documented recommendation logic in code comments & config | ✅ Fully Implemented |
| **FR-LEAD-01** | Lead Scoring | Numeric lead score starting at 0 per session | ✅ Fully Implemented |
| **FR-LEAD-02** | Lead Scoring | Points: Price (+5), 3+ products (+5), Compare (+10), Purchase intent (+20), Cart (+15) with duplicate action prevention | ✅ Fully Implemented |
| **FR-LEAD-03** | Lead Scoring | Classification into Cold (0–14), Warm (15–34), and Hot (35+) | ✅ Fully Implemented |
| **FR-LEAD-04** | Lead Scoring | Score and classification persisted against customer record in DB | ✅ Fully Implemented |
| **FR-CRM-01** | Internal CRM | Lead record creation on first interaction (session ID, contact, timestamp) | ✅ Fully Implemented |
| **FR-CRM-02** | Internal CRM | Full chat transcript logging per lead record | ✅ Fully Implemented |
| **FR-CRM-03** | Internal CRM | Real-time score & classification update after every interaction | ✅ Fully Implemented |
| **FR-CRM-04** | Internal CRM | Admin dashboard listing all leads, sortable by score, with full transcript inspection | ✅ Fully Implemented |
| **FR-PUR-01** | Cart & Checkout | Add products to simulated cart from chat or catalog | ✅ Fully Implemented |
| **FR-PUR-02** | Cart & Checkout | Order summary with quantities, items, and total price | ✅ Fully Implemented |
| **FR-PUR-03** | Cart & Checkout | Lead marked as "Converted" in CRM upon checkout | ✅ Fully Implemented |
| **NFR-MAIN-01** | Maintainability | Scoring points and recommendation rules in a single config file (`backend/app/config.py`) | ✅ Fully Implemented |
| **NFR-SEC-01** | Security | Customer contact details private to admin view only | ✅ Fully Implemented |
| **NFR-PORT-01** | Portability | Documented local execution for team and evaluators | ✅ Fully Implemented |



## 4. Lead Scoring Rules & Thresholds

Per SRS Section 3.4 and `backend/app/config.py`:

```python
LEAD_SCORING_POINTS = {
    "price_query": 5,        # Asking about price (+5)
    "viewed_3_products": 5,  # Viewing 3 or more products (+5)
    "compare_query": 10,     # Asking for a comparison (+10)
    "purchase_intent": 20,   # Mentioning intent to buy (+20)
    "added_to_cart": 15,     # Adding a product to cart (+15)
}

LEAD_THRESHOLDS = {
    "COLD_MAX": 14,          # Cold: 0 - 14
    "WARM_MIN": 15,          # Warm: 15 - 34
    "WARM_MAX": 34,
    "HOT_MIN": 35,           # Hot: 35+
}
```

*Note on Duplicate Prevention:* The system tracks triggered scoring actions per session in the database (`scored_actions`). Subsequent queries of the same intent will answer the customer accurately but will not repeatedly inflate the score.



## 5. Documented Simplifications for Tomorrow's Academic Demo

As formally scoped in **SRS.pdf Section 1.2 & Section 7**, the following deliberate boundaries were established for this academic mini-project:
1. **Rule-Based Intent Detection & Recommendation Engine:** Used structured pattern-matching and configurable tolerance rules (budget ±20%, category affinity, featured flags) instead of opaque, non-deterministic third-party ML/LLM API dependencies that can fail or rate-limit during a live presentation.
2. **Internal CRM Module:** Implemented an internal SQLite CRM module with admin monitoring and full transcript logs instead of a paid enterprise CRM integration (e.g. Salesforce or HubSpot).
3. **Simulated Checkout:** Replaced third-party payment gateways (Stripe/PayPal) with simulated checkout that validates customer name/contact, calculates totals, creates an order receipt, and marks the lead as converted.
4. **Single-Language Focus:** English language processing.



## 6. Setup and Execution Instructions

### Prerequisites
- Python 3.10+ (FastAPI, Uvicorn, SQLite)
- Node.js 18+ & npm

### Backend Setup & Launch
```bash
# 1. Navigate to backend directory
cd backend

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the FastAPI backend server
python run.py
```
*Backend API will run at:* `http://127.0.0.1:8000` (Swagger docs available at `http://127.0.0.1:8000/docs`).

### Frontend Setup & Launch
```bash
# 1. Open a new terminal in the frontend directory
cd frontend

# 2. Install dependencies (if not already installed)
npm install

# 3. Start the Vite React development server
npm run dev
```
*Frontend web application will run at:* `http://localhost:5173`.



## 7. 10-Step Academic Review Verification Walkthrough

To demonstrate the full project lifecycle during evaluation:

1. **Open Application:** Navigate to `http://localhost:5173`. Notice the top navigation bar with the live Lead Score pill: `Lead: 0 pts (COLD)` and the 24-product demo catalog.
2. **Budget Search:** In the AI Assistant chat window (or click quick prompt), ask:  
   `"Show me laptops under $1000"`  
   *Result:* Assistant detects `recommendation_request`, extracts budget `$1000`, evaluates ±20% tolerance, and displays matching laptops (e.g. Apple MacBook Air M2).
3. **Side-by-Side Comparison:** Ask:  
   `"Can you compare Apple MacBook Air M2 and Asus ZenBook 14?"`  
   *Result:* Intent `compare_query` is detected. Lead score increases by **+10** (Score: 10, Cold). Assistant displays a side-by-side spec and price matrix.
4. **Price Inquiry:** Ask:  
   `"What is the price of Apple MacBook Air M2?"`  
   *Result:* Intent `price_query` detected. Lead score increases by **+5** (Score: 15, **Warm** status reached!). Price ($999.00), stock status, and active rebate are shown.
5. **Add to Cart:** Click **Add to Cart** on the MacBook Air card.  
   *Result:* Lead score increases by **+15** (Score: 30, Warm). Cart icon badge updates to `1`.
6. **Express Purchase Intent:** In chat, type:  
   `"I want to purchase the MacBook Air right now"`  
   *Result:* Intent `purchase_intent` is detected. Lead score increases by **+20** (Score: 50, **HOT** status reached 🔥!).
7. **Complete Simulated Checkout:** Click the Cart icon, review the order summary ($999.00), enter Name (*e.g. Arun Evaluator*) and Email, and click **Complete Simulated Checkout**.  
   *Result:* Order is generated, order confirmation is displayed, and lead is marked as **Converted**.
8. **Admin CRM Review:** Switch to the **Admin CRM** tab in the top navigation bar.
9. **Verify Metrics:** Confirm Total Leads, Hot/Warm/Cold counts, and Conversions incremented in real-time.
10. **Inspect Customer Profile:** In the leads table, click **Inspect** on the lead. Review:
    - Customer Name and Contact details
    - Final Lead Score (`50 pts`) and Status (`HOT`)
    - Conversion badge: `✅ Converted`
    - Triggered scoring action history: `['compare_query', 'price_query', 'added_to_cart', 'purchase_intent']`
    - Simulated order record with total price
    - Full chronological conversation transcript with intent tags.



## 8. Automated Test Suites

Run the built-in automated test suites at any time:

```bash
# Run backend functional tests
python backend/test_backend.py

# Run complete 10-step end-to-end integration workflow test
python test_e2e_workflow.py
```

## License

This project is for academic purposes as part of the Jackfruit SE Mini-Project.

"""
Seeds realistic historical CRM leads and conversations for demo purposes.
Ensures the admin dashboard displays Hot, Warm, and Cold leads, conversion stats,
and rich chat history right out of the box for the academic presentation.
"""

import json
from datetime import datetime, timedelta
from .database import get_db_connection

SAMPLE_LEADS = [
    {
        "session_id": "sess_sophia_9812",
        "name": "Sophia Reynolds",
        "contact": "sophia.r@techcorp.io",
        "score": 55,
        "status": "Hot",
        "is_converted": 1,
        "scored_actions": ["price_query", "viewed_3_products", "compare_query", "purchase_intent", "added_to_cart"],
        "viewed_products": [1, 2, 3],
        "created_offset_hours": 3,
        "chat": [
            ("customer", "Hi! I need a fast ultrabook for software engineering, budget around $1500."),
            ("bot", "Hello Sophia! For high performance software engineering around $1500, I recommend the **Dell XPS 15 (9530)** ($1,499.00) and **Lenovo ThinkPad X1 Carbon Gen 11** ($1,349.00)."),
            ("customer", "How does the Dell XPS 15 compare to the Apple MacBook Air M2?"),
            ("bot", "Here is a comparison between Dell XPS 15 and Apple MacBook Air M2: Dell offers 14-core Intel i7, 16GB DDR5, and a 15.6-inch screen, while the MacBook Air offers fanless M2 efficiency and 18-hour battery."),
            ("customer", "What is the exact price and warranty on the Dell XPS 15?"),
            ("bot", "The Dell XPS 15 is $1,499.00 (In Stock). We also have an active deal: 10% OFF with Code XPS10!"),
            ("customer", "That sounds great, I want to purchase the Dell XPS 15."),
            ("bot", "Awesome choice! Added to your cart. Ready for simulated checkout!"),
            ("bot", "✅ Order #1001 Confirmed! Total: $1,499.00. Lead successfully converted.")
        ],
        "order": {
            "customer_name": "Sophia Reynolds",
            "customer_contact": "sophia.r@techcorp.io",
            "product_ids": [{"product_id": 2, "name": "Dell XPS 15 (9530)", "quantity": 1, "price": 1499.00}],
            "total_price": 1499.00
        }
    },
    {
        "session_id": "sess_marcus_4123",
        "name": "Marcus Chen",
        "contact": "mchen@gmail.com",
        "score": 40,
        "status": "Hot",
        "is_converted": 0,
        "scored_actions": ["compare_query", "purchase_intent", "price_query"],
        "viewed_products": [7, 8],
        "created_offset_hours": 6,
        "chat": [
            ("customer", "Hello, compare iPhone 15 Pro and Galaxy S24 Ultra."),
            ("bot", "Here is a side-by-side comparison: iPhone 15 Pro ($999.00) features Titanium build and A17 Pro chip. Samsung Galaxy S24 Ultra ($1,199.00) features a 200MP camera, Snapdragon 8 Gen 3, and integrated S Pen."),
            ("customer", "What is the price of the S24 Ultra?"),
            ("bot", "The Samsung Galaxy S24 Ultra is $1,199.00. We currently offer a $150 Trade-in Bonus."),
            ("customer", "I'm definitely planning to buy the S24 Ultra this weekend.")
        ],
        "order": None
    },
    {
        "session_id": "sess_elena_7821",
        "name": "Elena Rostova",
        "contact": "elena.design@studio.com",
        "score": 25,
        "status": "Warm",
        "is_converted": 0,
        "scored_actions": ["compare_query", "added_to_cart"],
        "viewed_products": [12, 13],
        "created_offset_hours": 12,
        "chat": [
            ("customer", "Hi, compare Sony WH-1000XM5 and Bose QuietComfort Ultra"),
            ("bot", "Sony WH-1000XM5 ($349.00) offers 30-hour battery and Auto NC Optimizer. Bose QuietComfort Ultra ($379.00) offers Bose Immersive Spatial Audio and legendary comfort."),
            ("customer", "Add Sony WH-1000XM5 to cart"),
            ("bot", "Added Sony WH-1000XM5 to your cart! You can view your cart or proceed to checkout.")
        ],
        "order": None
    },
    {
        "session_id": "sess_david_3391",
        "name": "David K.",
        "contact": None,
        "score": 10,
        "status": "Cold",
        "is_converted": 0,
        "scored_actions": ["price_query", "viewed_3_products"],
        "viewed_products": [16, 17, 18],
        "created_offset_hours": 24,
        "chat": [
            ("customer", "What is the price of Apple Watch Series 9?"),
            ("bot", "The Apple Watch Series 9 is $399.00 (In Stock). It includes 3 Months of Fitness+ free!"),
            ("customer", "Okay, thanks, just browsing.")
        ],
        "order": None
    }
]

def seed_demo_crm():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM leads")
    count = cursor.fetchone()[0]

    if count <= 1:
        base_time = datetime.now()
        for lead in SAMPLE_LEADS:
            created_dt = base_time - timedelta(hours=lead["created_offset_hours"])
            created_iso = created_dt.strftime("%Y-%m-%d %H:%M:%S")
            last_iso = (created_dt + timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
            INSERT OR REPLACE INTO leads (session_id, name, contact, score, status, created_at, last_interaction, is_converted, scored_actions, viewed_products)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                lead["session_id"],
                lead["name"],
                lead["contact"],
                lead["score"],
                lead["status"],
                created_iso,
                last_iso,
                lead["is_converted"],
                json.dumps(lead["scored_actions"]),
                json.dumps(lead["viewed_products"])
            ))
            lead_id = cursor.lastrowid

            # Seed chat logs
            for idx, (sender, msg) in enumerate(lead["chat"]):
                msg_time = (created_dt + timedelta(minutes=idx * 2)).strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("""
                INSERT INTO chat_logs (lead_id, session_id, sender, message, intent, extra_data, timestamp)
                VALUES (?, ?, ?, ?, 'demo_seeded', NULL, ?)
                """, (lead_id, lead["session_id"], sender, msg, msg_time))

            # Seed order if converted
            if lead["order"]:
                o = lead["order"]
                cursor.execute("""
                INSERT INTO orders (lead_id, session_id, customer_name, customer_contact, product_ids, total_price, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, 'Completed', ?)
                """, (
                    lead_id,
                    lead["session_id"],
                    o["customer_name"],
                    o["customer_contact"],
                    json.dumps(o["product_ids"]),
                    o["total_price"],
                    last_iso
                ))

        conn.commit()
    conn.close()

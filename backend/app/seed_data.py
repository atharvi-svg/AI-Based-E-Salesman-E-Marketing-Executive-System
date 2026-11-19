"""
Seed data generator for AI-Salesman demo product catalog.
Provides 24 realistic electronics products with detailed specifications,
categories, prices, stock statuses, featured status, and special offers.
"""

import json
from .database import get_db_connection

SAMPLE_PRODUCTS = [
    # Laptops
    {
        "id": 1,
        "name": "Apple MacBook Air M2",
        "category": "Laptops",
        "price": 999.00,
        "specs": {
            "processor": "Apple M2 8-core CPU",
            "ram": "8GB Unified Memory",
            "storage": "256GB SSD",
            "display": "13.6-inch Liquid Retina (2560x1664)",
            "battery": "Up to 18 hours",
            "weight": "1.24 kg",
            "os": "macOS Sonoma"
        },
        "stock_status": "In Stock",
        "is_featured": 1,
        "offer_flag": "$100 Instant Rebate",
        "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&auto=format&fit=crop&q=60",
        "description": "Supercharged by the M2 chip, remarkably thin and fast with brilliant Liquid Retina display."
    },
    {
        "id": 2,
        "name": "Dell XPS 15 (9530)",
        "category": "Laptops",
        "price": 1499.00,
        "specs": {
            "processor": "Intel Core i7-13700H (14-Core)",
            "ram": "16GB DDR5 4800MHz",
            "storage": "512GB PCIe NVMe SSD",
            "display": "15.6-inch FHD+ (1920x1200) InfinityEdge",
            "battery": "Up to 12 hours (86Wh)",
            "weight": "1.86 kg",
            "os": "Windows 11 Pro"
        },
        "stock_status": "In Stock",
        "is_featured": 1,
        "offer_flag": "10% OFF with Code XPS10",
        "image_url": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500&auto=format&fit=crop&q=60",
        "description": "Masterfully crafted performance laptop featuring premium aluminum chassis and edge-to-edge screen."
    },
    {
        "id": 3,
        "name": "Asus ZenBook 14 OLED",
        "category": "Laptops",
        "price": 799.00,
        "specs": {
            "processor": "Intel Core Ultra 7 155H",
            "ram": "16GB LPDDR5X",
            "storage": "1TB M.2 NVMe SSD",
            "display": "14.0-inch 3K (2880x1800) OLED 120Hz",
            "battery": "Up to 15 hours (75Wh)",
            "weight": "1.20 kg",
            "os": "Windows 11 Home"
        },
        "stock_status": "In Stock",
        "is_featured": 1,
        "offer_flag": "Student Special: Free Sleeve",
        "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&auto=format&fit=crop&q=60",
        "description": "Ultraportable AI-ready laptop with breathtaking 3K OLED HDR screen and all-day battery life."
    },
    {
        "id": 4,
        "name": "Lenovo ThinkPad X1 Carbon Gen 11",
        "category": "Laptops",
        "price": 1349.00,
        "specs": {
            "processor": "Intel Core i7-1365U vPro",
            "ram": "16GB LPDDR5",
            "storage": "512GB SSD OPAL2.0",
            "display": "14-inch WUXGA (1920x1200) IPS Anti-glare",
            "battery": "Up to 14 hours (57Wh)",
            "weight": "1.12 kg",
            "os": "Windows 11 Pro"
        },
        "stock_status": "Limited Stock",
        "is_featured": 0,
        "offer_flag": None,
        "image_url": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=500&auto=format&fit=crop&q=60",
        "description": "The quintessential business ultrabook: featherweight carbon-fiber build, legendary keyboard, and military-grade durability."
    },
    {
        "id": 5,
        "name": "HP Envy x360 2-in-1",
        "category": "Laptops",
        "price": 699.00,
        "specs": {
            "processor": "AMD Ryzen 7 7730U",
            "ram": "16GB DDR4",
            "storage": "512GB SSD",
            "display": "15.6-inch FHD Touchscreen 360 convertible",
            "battery": "Up to 11 hours",
            "weight": "1.79 kg",
            "os": "Windows 11 Home"
        },
        "stock_status": "In Stock",
        "is_featured": 0,
        "offer_flag": "Save $80 Today",
        "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500&auto=format&fit=crop&q=60",
        "description": "Versatile 360-degree convertible laptop designed for seamless note-taking, sketching, and entertainment."
    },
    {
        "id": 6,
        "name": "Acer Swift Go 14",
        "category": "Laptops",
        "price": 649.00,
        "specs": {
            "processor": "Intel Core i5-1335U",
            "ram": "8GB LPDDR5",
            "storage": "512GB PCIe Gen 4 SSD",
            "display": "14-inch IPS Full HD 100% sRGB",
            "battery": "Up to 10 hours",
            "weight": "1.25 kg",
            "os": "Windows 11 Home"
        },
        "stock_status": "In Stock",
        "is_featured": 0,
        "offer_flag": "Best Budget Pick",
        "image_url": "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=500&auto=format&fit=crop&q=60",
        "description": "Lightweight everyday laptop with vibrant display, dual fans cooling, and multi-port connectivity."
    },

    # Smartphones
    {
        "id": 7,
        "name": "Apple iPhone 15 Pro",
        "category": "Smartphones",
        "price": 999.00,
        "specs": {
            "processor": "A17 Pro chip (3nm)",
            "ram": "8GB",
            "storage": "128GB",
            "display": "6.1-inch Super Retina XDR OLED 120Hz ProMotion",
            "camera": "48MP Main + 12MP Ultra-wide + 12MP 3x Telephoto",
            "battery": "Up to 23 hours video",
            "os": "iOS 17"
        },
        "stock_status": "In Stock",
        "is_featured": 1,
        "offer_flag": "Free MagSafe Charger with Purchase",
        "image_url": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=500&auto=format&fit=crop&q=60",
        "description": "Forged in aerospace-grade titanium with game-changing A17 Pro chip and customizable Action button."
    },
    {
        "id": 8,
        "name": "Samsung Galaxy S24 Ultra",
        "category": "Smartphones",
        "price": 1199.00,
        "specs": {
            "processor": "Snapdragon 8 Gen 3 for Galaxy",
            "ram": "12GB",
            "storage": "256GB",
            "display": "6.8-inch Dynamic AMOLED 2X QHD+ (2600 nits)",
            "camera": "200MP Main + 50MP 5x Periscope + 12MP UW + 10MP 3x",
            "battery": "5000 mAh (45W fast charge)",
            "os": "Android 14 (One UI 6.1)"
        },
        "stock_status": "In Stock",
        "is_featured": 1,
        "offer_flag": "$150 Trade-in Bonus",
        "image_url": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=500&auto=format&fit=crop&q=60",
        "description": "The pinnacle of Android engineering: integrated S Pen stylus, Galaxy AI suite, and 200MP pro camera."
    },
    {
        "id": 9,
        "name": "Google Pixel 8 Pro",
        "category": "Smartphones",
        "price": 799.00,
        "specs": {
            "processor": "Google Tensor G3",
            "ram": "12GB",
            "storage": "128GB",
            "display": "6.7-inch Super Actua LTPO OLED (1-120Hz)",
            "camera": "50MP Main + 48MP UW + 48MP 5x Telephoto",
            "battery": "5050 mAh (30W fast charge)",
            "os": "Android 14 (7 years updates)"
        },
        "stock_status": "In Stock",
        "is_featured": 1,
        "offer_flag": "Save $200 Limited Offer",
        "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&auto=format&fit=crop&q=60",
        "description": "Engineered by Google with AI at its core: industry-leading computational photography and Best Take magic editor."
    },
    {
        "id": 10,
        "name": "OnePlus 12",
        "category": "Smartphones",
        "price": 699.00,
        "specs": {
            "processor": "Snapdragon 8 Gen 3",
            "ram": "16GB LPDDR5X",
            "storage": "256GB UFS 4.0",
            "display": "6.82-inch 2K ProXDR 120Hz Display",
            "camera": "50MP Sony LYT-808 + 64MP 3x Periscope + 48MP UW",
            "battery": "5400 mAh (80W SUPERVOOC charging)",
            "os": "OxygenOS 14"
        },
        "stock_status": "In Stock",
        "is_featured": 0,
        "offer_flag": "Includes 80W Charger in Box",
        "image_url": "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=500&auto=format&fit=crop&q=60",
        "description": "Flagship powerhouse with Hasselblad 4th Gen camera system and hyper-fast 80W charging."
    },
    {
        "id": 11,
        "name": "Samsung Galaxy A54 5G",
        "category": "Smartphones",
        "price": 379.00,
        "specs": {
            "processor": "Exynos 1380",
            "ram": "6GB",
            "storage": "128GB (Expandable microSD)",
            "display": "6.4-inch Super AMOLED 120Hz FHD+",
            "camera": "50MP OIS + 12MP UW + 5MP Macro",
            "battery": "5000 mAh (2-day battery)",
            "os": "Android 14"
        },
        "stock_status": "In Stock",
        "is_featured": 0,
        "offer_flag": "Great Value Pick",
        "image_url": "https://images.unsplash.com/photo-1567581935884-3349723552ca?w=500&auto=format&fit=crop&q=60",
        "description": "Premium glass finish, IP67 water resistance, and crystal-clear AMOLED display at a budget-friendly price."
    },

    # Audio & Headphones
    {
        "id": 12,
        "name": "Sony WH-1000XM5",
        "category": "Audio",
        "price": 349.00,
        "specs": {
            "type": "Over-Ear Wireless",
            "noise_canceling": "Dual Processor Auto NC Optimizer",
            "battery": "Up to 30 hours (3 min charge = 3 hours)",
            "drivers": "30mm Precision engineered carbon fiber dome",
            "weight": "250g",
            "connectivity": "Bluetooth 5.2, Multipoint, LDAC"
        },
        "stock_status": "In Stock",
        "is_featured": 1,
        "offer_flag": "15% OFF This Weekend",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60",
        "description": "Industry-leading active noise cancellation with 8 microphones and ultra-comfortable lightweight design."
    },
    {
        "id": 13,
        "name": "Bose QuietComfort Ultra",
        "category": "Audio",
        "price": 379.00,
        "specs": {
            "type": "Over-Ear Wireless",
            "noise_canceling": "World-Class Active Noise Canceling + Aware Mode",
            "battery": "Up to 24 hours (18 with Immersive Audio)",
            "features": "Bose Immersive Spatial Audio, CustomTune tech",
            "weight": "253g",
            "connectivity": "Bluetooth 5.3, Snapdragon Sound"
        },
        "stock_status": "In Stock",
        "is_featured": 0,
        "offer_flag": None,
        "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=500&auto=format&fit=crop&q=60",
        "description": "Breakthrough spatialized audio places sound directly in front of you for unprecedented listening immersion."
    },
    {
        "id": 14,
        "name": "Apple AirPods Pro (2nd Gen, USB-C)",
        "category": "Audio",
        "price": 249.00,
        "specs": {
            "type": "In-Ear True Wireless",
            "noise_canceling": "2x more Active Noise Cancellation + Transparency",
            "chip": "Apple H2 chip",
            "battery": "6 hours (30 hours with MagSafe USB-C case)",
            "water_resistance": "IP54 dust, sweat, and water resistant",
            "connectivity": "Bluetooth 5.3"
        },
        "stock_status": "In Stock",
        "is_featured": 1,
        "offer_flag": "Free Engraving Available",
        "image_url": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=500&auto=format&fit=crop&q=60",
        "description": "Adaptive Audio dynamically blends Transparency and Active Noise Cancellation tailored to your environment."
    },
    {
        "id": 15,
        "name": "Sennheiser Momentum 4 Wireless",
        "category": "Audio",
        "price": 279.00,
        "specs": {
            "type": "Over-Ear Wireless",
            "battery": "Incredible 60 hours battery life",
            "noise_canceling": "Adaptive Noise Cancellation",
            "drivers": "Audiophile-inspired 42mm transducer system",
            "weight": "293g",
            "connectivity": "Bluetooth 5.2, aptX Adaptive"
        },
        "stock_status": "Limited Stock",
        "is_featured": 0,
        "offer_flag": "$50 Off Special",
        "image_url": "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=500&auto=format&fit=crop&q=60",
        "description": "Signature Sennheiser sound clarity with an unmatched 60-hour playtime on a single charge."
    },

    # Smartwatches & Wearables
    {
        "id": 16,
        "name": "Apple Watch Series 9",
        "category": "Smartwatches",
        "price": 399.00,
        "specs": {
            "processor": "S9 SiP with 4-core Neural Engine",
            "display": "Always-On Retina display (up to 2000 nits)",
            "case_size": "45mm Aluminum Case",
            "sensors": "Blood Oxygen, ECG, Temperature sensing, Heart Rate",
            "battery": "18 hours (36 hours in Low Power Mode)",
            "features": "Double Tap gesture, Siri on-device"
        },
        "stock_status": "In Stock",
        "is_featured": 1,
        "offer_flag": "Free 3 Months Fitness+",
        "image_url": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=500&auto=format&fit=crop&q=60",
        "description": "Smarter, brighter, and mightier: magic new Double Tap gesture and on-device health intelligence."
    },
    {
        "id": 17,
        "name": "Samsung Galaxy Watch 6 Classic",
        "category": "Smartwatches",
        "price": 349.00,
        "specs": {
            "processor": "Exynos W930 Dual-Core 1.4GHz",
            "display": "1.5-inch Super AMOLED Sapphire Crystal",
            "bezel": "Physical Rotating Bezel",
            "sensors": "BioActive Sensor (HR, ECG, BIA Body Composition)",
            "battery": "Up to 40 hours (425 mAh)",
            "os": "Wear OS Powered by Samsung"
        },
        "stock_status": "In Stock",
        "is_featured": 0,
        "offer_flag": "10% Bundle Discount",
        "image_url": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=500&auto=format&fit=crop&q=60",
        "description": "Timeless mechanical rotating bezel design with advanced sleep coaching and in-depth body composition insights."
    },
    {
        "id": 18,
        "name": "Garmin Forerunner 265",
        "category": "Smartwatches",
        "price": 449.00,
        "specs": {
            "display": "1.3-inch Colorful AMOLED Touchscreen",
            "battery": "Up to 13 days in smartwatch mode (20 hrs GPS)",
            "gps": "Multi-Band GNSS with SatIQ technology",
            "metrics": "Training Readiness, HRV Status, VO2 Max, Race Widget",
            "water_rating": "5 ATM"
        },
        "stock_status": "In Stock",
        "is_featured": 0,
        "offer_flag": None,
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&auto=format&fit=crop&q=60",
        "description": "Dedicated running and triathlon GPS smartwatch with brilliant AMOLED display and detailed recovery science."
    },

    # Tablets
    {
        "id": 19,
        "name": "Apple iPad Air M2 (11-inch)",
        "category": "Tablets",
        "price": 599.00,
        "specs": {
            "processor": "Apple M2 chip",
            "ram": "8GB",
            "storage": "128GB",
            "display": "11-inch Liquid Retina with True Tone and P3 wide color",
            "camera": "Landscape 12MP Ultra Wide front camera with Center Stage",
            "battery": "Up to 10 hours",
            "compatibility": "Apple Pencil Pro, Magic Keyboard"
        },
        "stock_status": "In Stock",
        "is_featured": 1,
        "offer_flag": "$50 Educational Savings",
        "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500&auto=format&fit=crop&q=60",
        "description": "Freshly redesigned with the powerful M2 chip, support for Apple Pencil Pro, and landscape front camera."
    },
    {
        "id": 20,
        "name": "Samsung Galaxy Tab S9 FE",
        "category": "Tablets",
        "price": 449.00,
        "specs": {
            "processor": "Exynos 1380",
            "ram": "6GB",
            "storage": "128GB (MicroSD up to 1TB)",
            "display": "10.9-inch 90Hz WQXGA Display",
            "water_resistance": "IP68 water and dust resistant (tablet + S Pen)",
            "stylus": "S Pen included in box",
            "battery": "8000 mAh (45W fast charge)"
        },
        "stock_status": "In Stock",
        "is_featured": 0,
        "offer_flag": "Includes S Pen ($60 Value)",
        "image_url": "https://images.unsplash.com/photo-1561154464-82e9adf32764?w=500&auto=format&fit=crop&q=60",
        "description": "Rugged IP68 water-resistant tablet with included S Pen for students, artists, and outdoor note-taking."
    },
    {
        "id": 21,
        "name": "Microsoft Surface Pro 9",
        "category": "Tablets",
        "price": 899.00,
        "specs": {
            "processor": "12th Gen Intel Core i5-1235U",
            "ram": "8GB LPDDR5",
            "storage": "256GB Removable SSD",
            "display": "13-inch PixelSense Flow Display (2880x1920) 120Hz",
            "battery": "Up to 15.5 hours",
            "weight": "879g",
            "os": "Windows 11 Home"
        },
        "stock_status": "Limited Stock",
        "is_featured": 0,
        "offer_flag": "Save $100 on Surface Bundle",
        "image_url": "https://images.unsplash.com/photo-1585792180666-f75a7c52b278?w=500&auto=format&fit=crop&q=60",
        "description": "2-in-1 versatility of a tablet with the power of a laptop, built-in kickstand, and Thunderbolt 4 ports."
    },

    # Accessories & Monitors
    {
        "id": 22,
        "name": "Dell UltraSharp 27 4K Monitor (U2723QE)",
        "category": "Accessories",
        "price": 549.00,
        "specs": {
            "panel": "27-inch IPS Black 4K UHD (3840x2160)",
            "contrast_ratio": "2000:1 contrast ratio with VESA DisplayHDR 400",
            "color": "100% sRGB, 98% DCI-P3",
            "connectivity": "USB-C Hub (90W Power Delivery), RJ45 Ethernet, DP 1.4, HDMI",
            "stand": "Height, tilt, swivel, and pivot adjustable"
        },
        "stock_status": "In Stock",
        "is_featured": 1,
        "offer_flag": "Top Creator Pick",
        "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=500&auto=format&fit=crop&q=60",
        "description": "Groundbreaking IPS Black technology delivers double the contrast ratio and comprehensive USB-C single-cable connectivity."
    },
    {
        "id": 23,
        "name": "Logitech MX Master 3S Wireless Mouse",
        "category": "Accessories",
        "price": 99.00,
        "specs": {
            "sensor": "8000 DPI Darkfield tracking (works on glass)",
            "clicks": "Quiet Click technology (90% less noise)",
            "scroll": "MagSpeed Electromagnetic scrolling (1000 lines/sec)",
            "battery": "Up to 70 days (1 min charge = 3 hours)",
            "connectivity": "Bluetooth Low Energy + Logi Bolt USB"
        },
        "stock_status": "In Stock",
        "is_featured": 0,
        "offer_flag": "Best Ergonomic Mouse",
        "image_url": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=500&auto=format&fit=crop&q=60",
        "description": "Iconic ergonomic mouse remastered with quiet clicks and an 8K DPI sensor for speed and precision on any surface."
    },
    {
        "id": 24,
        "name": "Keychron Q1 Pro Wireless Mechanical Keyboard",
        "category": "Accessories",
        "price": 199.00,
        "specs": {
            "layout": "75% compact layout with CNC Aluminum body",
            "switches": "K Pro Banana / Red hot-swappable switches",
            "connectivity": "Bluetooth 5.1 + Type-C wired",
            "keycaps": "Double-shot KSA PBT keycaps",
            "customization": "QMK/VIA fully programmable"
        },
        "stock_status": "In Stock",
        "is_featured": 0,
        "offer_flag": "Free Keycap Puller included",
        "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500&auto=format&fit=crop&q=60",
        "description": "Audiophile-grade custom mechanical keyboard encased in a heavy CNC machined aluminum body with double-gasket dampening."
    }
]

def seed_products(force: bool = False):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]

    if count == 0 or force:
        if force:
            cursor.execute("DELETE FROM products")

        for p in SAMPLE_PRODUCTS:
            cursor.execute("""
            INSERT INTO products (id, name, category, price, specs, stock_status, is_featured, offer_flag, image_url, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p["id"],
                p["name"],
                p["category"],
                p["price"],
                json.dumps(p["specs"]),
                p["stock_status"],
                p["is_featured"],
                p["offer_flag"],
                p["image_url"],
                p["description"]
            ))
        conn.commit()
    conn.close()

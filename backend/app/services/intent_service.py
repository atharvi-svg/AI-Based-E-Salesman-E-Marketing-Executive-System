"""
Intent detection and entity extraction service.
Implements FR-CHAT-04 and FR-CHAT-05.
Detects:
- price_query
- spec_query
- compare_query
- offer_query
- recommendation_request
- purchase_intent
- general/greeting
- unknown
"""

import re
from typing import Dict, Any, List, Optional, Tuple

class IntentService:
    @staticmethod
    def extract_budget(text: str) -> Optional[float]:
        """
        Extract numerical budget mentioned in the query.
        Handles: "under $1000", "below 800", "budget of 1200", "around $500", "within 900", etc.
        """
        patterns = [
            r'(?:under|below|less than|up to|within|max(?:imum)? of|budget(?: of)?)\s*[\$₹€£]?\s*(\d+(?:,\d+)*(?:\.\d+)?)',
            r'[\$₹€£]\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:budget|or less|max)',
            r'around\s*[\$₹€£]?\s*(\d+(?:,\d+)*(?:\.\d+)?)',
            r'[\$₹€£]\s*(\d+(?:,\d+)*(?:\.\d+)?)'
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                val_str = match.group(1).replace(',', '')
                try:
                    val = float(val_str)
                    if val > 10:  # avoid noise like small numbers
                        return val
                except ValueError:
                    pass
        return None

    @staticmethod
    def extract_category(text: str) -> Optional[str]:
        """
        Identify the product category mentioned in text.
        """
        text_lower = text.lower()
        if any(w in text_lower for w in ["laptop", "laptops", "notebook", "macbook", "zenbook", "thinkpad", "ultrabook", "pc"]):
            return "Laptops"
        if any(w in text_lower for w in ["phone", "phones", "smartphone", "smartphones", "iphone", "galaxy", "pixel", "oneplus", "mobile"]):
            return "Smartphones"
        if any(w in text_lower for w in ["headphone", "headphones", "earbuds", "earphones", "airpods", "audio", "sound", "headset"]):
            return "Audio"
        if any(w in text_lower for w in ["watch", "watches", "smartwatch", "smartwatches", "wearable", "garmin"]):
            return "Smartwatches"
        if any(w in text_lower for w in ["tablet", "tablets", "ipad", "surface", "tab"]):
            return "Tablets"
        if any(w in text_lower for w in ["monitor", "mouse", "keyboard", "accessories", "accessory", "display", "screen"]):
            return "Accessories"
        return None

    @staticmethod
    def extract_product_candidates(text: str, all_products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Match specific products from catalog referenced in text by specific model identifiers.
        """
        text_lower = text.lower()
        matched = []

        # Product-specific distinct keywords mapped to product names or parts
        for p in all_products:
            name_lower = p["name"].lower()
            # 1. Full name match
            if name_lower in text_lower:
                if p not in matched:
                    matched.append(p)
                continue

            # 2. Distinct model identifier patterns
            # E.g. 'macbook air', 'zenbook', 'xps 15', 'thinkpad', 'envy x360', 'swift go',
            # 'iphone 15', 's24 ultra', 'pixel 8', 'oneplus 12', 'galaxy a54',
            # 'wh-1000xm5', 'quietcomfort', 'airpods pro', 'momentum 4',
            # 'watch series 9', 'galaxy watch', 'forerunner 265',
            # 'ipad air', 'tab s9', 'surface pro 9',
            # 'ultrasharp', 'mx master', 'keychron q1'
            model_identifiers = {
                1: ["macbook", "macbook air", "m2 air"],
                2: ["xps", "dell xps", "xps 15"],
                3: ["zenbook", "asus zenbook", "zenbook 14"],
                4: ["thinkpad", "x1 carbon"],
                5: ["envy x360", "hp envy"],
                6: ["swift go", "acer swift"],
                7: ["iphone", "iphone 15", "15 pro"],
                8: ["s24", "galaxy s24", "s24 ultra"],
                9: ["pixel 8", "pixel 8 pro", "google pixel"],
                10: ["oneplus", "oneplus 12"],
                11: ["galaxy a54", "a54"],
                12: ["wh-1000xm5", "xm5", "sony wh"],
                13: ["quietcomfort", "bose ultra", "qc ultra"],
                14: ["airpods pro", "airpods"],
                15: ["momentum 4", "sennheiser momentum"],
                16: ["watch series 9", "apple watch"],
                17: ["watch 6 classic", "galaxy watch"],
                18: ["forerunner", "garmin forerunner"],
                19: ["ipad air", "ipad"],
                20: ["tab s9", "galaxy tab"],
                21: ["surface pro", "surface pro 9"],
                22: ["ultrasharp", "u2723qe"],
                23: ["mx master", "mx master 3s"],
                24: ["keychron", "q1 pro"]
            }

            prod_id = p["id"]
            if prod_id in model_identifiers:
                for identifier in model_identifiers[prod_id]:
                    if identifier in text_lower:
                        if p not in matched:
                            matched.append(p)
                        break

        return matched

    @classmethod
    def detect_intent(cls, message: str) -> Tuple[str, Dict[str, Any]]:
        """
        Classifies user query into one of:
        - price_query
        - spec_query
        - compare_query
        - offer_query
        - recommendation_request
        - purchase_intent
        - general/greeting
        - unknown
        """
        text = message.strip()
        text_lower = text.lower()
        metadata: Dict[str, Any] = {}

        budget = cls.extract_budget(text)
        if budget:
            metadata["budget"] = budget

        category = cls.extract_category(text)
        if category:
            metadata["category"] = category

        # 1. Compare Query (High precedence)
        compare_patterns = [
            r'\bcompare\b', r'\bvs\b', r'\bversus\b', r'\bdifference between\b',
            r'\bwhich is better\b', r'\bhow does .* compare\b', r'\bbetter than\b'
        ]
        if any(re.search(pat, text_lower) for pat in compare_patterns):
            return "compare_query", metadata

        # 2. Purchase Intent
        purchase_patterns = [
            r'\bbuy\b', r'\bpurchase\b', r'\border\b', r'\bcheckout\b',
            r'\badd to cart\b', r'\bi want to buy\b', r'\bi will take\b',
            r'\bhow can i pay\b', r'\bget this now\b', r'\bready to order\b'
        ]
        if any(re.search(pat, text_lower) for pat in purchase_patterns):
            return "purchase_intent", metadata

        # 3. Price Query
        price_patterns = [
            r'\bprice\b', r'\bhow much\b', r'\bcost\b', r'\bpricing\b',
            r'\bhow expensive\b', r'\brate\b', r'\bcheap\b', r'\baffordable\b'
        ]
        if any(re.search(pat, text_lower) for pat in price_patterns) and not ("recommend" in text_lower or "suggest" in text_lower):
            return "price_query", metadata

        # 4. Offers / Deals / Discounts Query
        offer_patterns = [
            r'\boffer\b', r'\boffers\b', r'\bdeal\b', r'\bdeals\b', r'\bdiscount\b',
            r'\bdiscounts\b', r'\bcoupon\b', r'\bpromo\b', r'\bsale\b', r'\brebate\b'
        ]
        if any(re.search(pat, text_lower) for pat in offer_patterns):
            return "offer_query", metadata

        # 5. Recommendation / Advice Query
        rec_patterns = [
            r'\brecommend\b', r'\bsuggest\b', r'\bshow me\b', r'\blooking for\b',
            r'\bfind me\b', r'\bwhat should i buy\b', r'\bunder \d+\b', r'\boptions for\b',
            r'\btop picks\b', r'\bbest\b', r'\bpopular\b', r'\bfeatured\b'
        ]
        if any(re.search(pat, text_lower) for pat in rec_patterns) or budget is not None:
            return "recommendation_request", metadata

        # 6. Specifications / Details Query
        spec_patterns = [
            r'\bspec\b', r'\bspecs\b', r'\bspecification\b', r'\bfeatures\b',
            r'\bram\b', r'\bbattery\b', r'\bdisplay\b', r'\bscreen\b', r'\bprocessor\b',
            r'\bstorage\b', r'\bcamera\b', r'\bweight\b', r'\bperformance\b', r'\bdetails\b'
        ]
        if any(re.search(pat, text_lower) for pat in spec_patterns):
            return "spec_query", metadata

        # 7. General / Greeting
        greeting_patterns = [
            r'\bhi\b', r'\bhello\b', r'\bhey\b', r'\bgood morning\b', r'\bgood afternoon\b',
            r'\bgood evening\b', r'\bhowdy\b', r'\bwho are you\b', r'\bwhat can you do\b',
            r'\bhelp\b', r'\bthanks\b', r'\bthank you\b', r'\bbye\b', r'\bgoodbye\b'
        ]
        if any(re.search(pat, text_lower) for pat in greeting_patterns):
            return "general/greeting", metadata

        # If a category is mentioned by itself (e.g. "Laptops" or "show smartphones")
        if category:
            return "recommendation_request", metadata

        # 8. Unknown (Clarification required per FR-CHAT-05)
        return "unknown", metadata

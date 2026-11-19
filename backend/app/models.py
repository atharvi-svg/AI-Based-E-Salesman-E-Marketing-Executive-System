"""
Pydantic data models & request/response schemas for AI-Salesman API.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Product(BaseModel):
    id: int
    name: str
    category: str
    price: float
    specs: Dict[str, Any]
    stock_status: str
    is_featured: bool
    offer_flag: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None

class ProductComparison(BaseModel):
    product_a: Product
    product_b: Product
    differences: Dict[str, Any]

class ChatMessageRequest(BaseModel):
    session_id: str
    message: str
    user_name: Optional[str] = None
    user_contact: Optional[str] = None

class ChatMessageResponse(BaseModel):
    session_id: str
    reply: str
    intent: str
    lead_score: int
    lead_status: str
    score_increment: int = 0
    scored_reason: Optional[str] = None
    products: Optional[List[Product]] = None
    comparison: Optional[Dict[str, Any]] = None
    suggested_prompts: Optional[List[str]] = None

class AddToCartRequest(BaseModel):
    session_id: str
    product_id: int
    quantity: int = 1

class CartItem(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int
    image_url: Optional[str] = None

class CheckoutRequest(BaseModel):
    session_id: str
    customer_name: str
    customer_contact: str
    items: List[CartItem]
    total_price: float

class CheckoutResponse(BaseModel):
    order_id: int
    lead_id: int
    session_id: str
    total_price: float
    status: str
    message: str

class LeadRecord(BaseModel):
    id: int
    session_id: str
    name: Optional[str] = None
    contact: Optional[str] = None
    score: int
    status: str
    created_at: str
    last_interaction: str
    is_converted: bool
    scored_actions: List[str]

class ChatLogItem(BaseModel):
    id: int
    sender: str
    message: str
    intent: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None
    timestamp: str

class LeadDetailResponse(BaseModel):
    lead: LeadRecord
    chat_logs: List[ChatLogItem]
    orders: List[Dict[str, Any]]

class AdminMetrics(BaseModel):
    total_leads: int
    hot_leads: int
    warm_leads: int
    cold_leads: int
    total_conversions: int
    conversion_rate: float
    total_revenue: float

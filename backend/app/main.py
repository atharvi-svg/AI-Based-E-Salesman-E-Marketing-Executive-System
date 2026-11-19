"""
FastAPI Application Entrypoint for AI-Salesman & E-Marketing Executive System.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .seed_data import seed_products
from .seed_crm import seed_demo_crm
from .routers import products, chat, cart, admin

app = FastAPI(
    title="AI-Salesman & E-Marketing Executive API",
    description="Backend REST API for AI-based virtual sales assistant and internal CRM.",
    version="2.0.0"
)

# Enable CORS for frontend client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products.router)
app.include_router(chat.router)
app.include_router(cart.router)
app.include_router(admin.router)

@app.on_event("startup")
def startup_event():
    init_db()
    seed_products()
    seed_demo_crm()

@app.get("/")
def root():
    return {
        "project": "AI-Based E-Salesman & E-Marketing Executive System",
        "team": "Code Connect",
        "status": "online",
        "docs_url": "/docs"
    }

@app.get("/api/health")
def health():
    return {"status": "healthy"}

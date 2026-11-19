"""
Database management for AI-Salesman using SQLite.
Implements the tables specified in SRS Section 6.3:
- products
- leads
- chat_logs
- orders
"""

import sqlite3
import json
import os
from datetime import datetime
from .config import DB_PATH

def get_db_connection():
    # Ensure directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        specs TEXT NOT NULL,
        stock_status TEXT NOT NULL,
        is_featured INTEGER NOT NULL DEFAULT 0,
        offer_flag TEXT,
        image_url TEXT,
        description TEXT
    );
    """)

    # 2. Leads table (CRM)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT UNIQUE NOT NULL,
        name TEXT,
        contact TEXT,
        score INTEGER NOT NULL DEFAULT 0,
        status TEXT NOT NULL DEFAULT 'Cold',
        created_at TEXT NOT NULL,
        last_interaction TEXT NOT NULL,
        is_converted INTEGER NOT NULL DEFAULT 0,
        scored_actions TEXT NOT NULL DEFAULT '[]',
        viewed_products TEXT NOT NULL DEFAULT '[]'
    );
    """)

    # 3. Chat logs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lead_id INTEGER,
        session_id TEXT NOT NULL,
        sender TEXT NOT NULL,
        message TEXT NOT NULL,
        intent TEXT,
        extra_data TEXT,
        timestamp TEXT NOT NULL
    );
    """)

    # 4. Orders table (Simulated checkout)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lead_id INTEGER,
        session_id TEXT NOT NULL,
        customer_name TEXT NOT NULL,
        customer_contact TEXT NOT NULL,
        product_ids TEXT NOT NULL,
        total_price REAL NOT NULL,
        status TEXT NOT NULL DEFAULT 'Completed',
        created_at TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()

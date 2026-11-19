"""
Chat API router.
"""

import json
from typing import List, Dict, Any
from fastapi import APIRouter
from ..models import ChatMessageRequest, ChatMessageResponse, ChatLogItem
from ..services.chat_service import ChatService
from ..database import get_db_connection

router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.post("", response_model=ChatMessageResponse)
def post_chat_message(payload: ChatMessageRequest):
    result = ChatService.process_message(
        session_id=payload.session_id,
        user_message=payload.message,
        user_name=payload.user_name,
        user_contact=payload.user_contact
    )
    return ChatMessageResponse(**result)

@router.get("/history/{session_id}", response_model=List[ChatLogItem])
def get_chat_history(session_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, sender, message, intent, extra_data, timestamp
    FROM chat_logs
    WHERE session_id = ?
    ORDER BY id ASC
    """, (session_id,))
    rows = cursor.fetchall()
    conn.close()

    history = []
    for r in rows:
        item = dict(r)
        if item.get("extra_data"):
            item["extra_data"] = json.loads(item["extra_data"])
        history.append(ChatLogItem(**item))

    return history

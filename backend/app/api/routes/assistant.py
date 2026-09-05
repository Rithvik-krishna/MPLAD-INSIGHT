"""
FastAPI Routes for NIDHI Assistant AI Audit Copilot
Provides /api/assistant/chat and /api/assistant/status
"""

from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional, Any
import sys
from pathlib import Path

# Ensure root is in path for assistant_service
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from backend.assistant_service import handle_chat_request, NVIDIA_MODEL, RATE_LIMIT_PER_MINUTE, RATE_LIMIT_PER_HOUR
except ImportError:
    from assistant_service import handle_chat_request, NVIDIA_MODEL, RATE_LIMIT_PER_MINUTE, RATE_LIMIT_PER_HOUR

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    pageContext: Optional[dict[str, Any]] = None
    conversation: Optional[list[dict[str, Any]]] = None

@router.get("/status")
def get_assistant_status():
    return {
        "name": "NIDHI Assistant",
        "subtitle": "AI Audit Copilot",
        "status": "online",
        "mode": "live",
        "model": NVIDIA_MODEL,
        "rateLimitPerMinute": RATE_LIMIT_PER_MINUTE,
        "rateLimitPerHour": RATE_LIMIT_PER_HOUR,
    }

@router.post("/chat")
async def chat_copilot(req: ChatRequest, request: Request):
    client_ip = request.client.host if request.client else "127.0.0.1"
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        client_ip = forwarded.split(",")[0].strip()

    body = {
        "message": req.message,
        "pageContext": req.pageContext or {},
        "conversation": req.conversation or []
    }
    return handle_chat_request(body, client_ip=client_ip)

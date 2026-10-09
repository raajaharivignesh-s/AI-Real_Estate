from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from app.db.models import User
from app.api.deps import get_current_user
from app.services.llm import LLMService

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    reply: str

llm_service = LLMService()

@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, current_user: User = Depends(get_current_user)):
    # Convert Pydantic to dict
    messages = [{"role": m.role, "content": m.content} for m in request.messages]
    
    # Prepend system prompt
    system_msg = {
        "role": "system",
        "content": f"You are a helpful Real Estate AI Assistant. You are assisting {current_user.full_name}."
    }
    messages.insert(0, system_msg)
    
    reply = await llm_service.chat(messages, current_user.id)
    return ChatResponse(reply=reply)

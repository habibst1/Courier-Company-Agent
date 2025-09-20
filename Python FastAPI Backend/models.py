# models.py
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class QueryRequest(BaseModel):
    question: str
    user_id: Optional[int] = None
    tracking_number: Optional[str] = None

class QueryResponse(BaseModel):
    type: str  # 'results', 'clarification', 'error', 'general'
    query: Optional[str] = None
    data: Optional[List[Dict[str, Any]]] = None
    message: Optional[str] = None
    response: Optional[str] = None

class ConversationHistoryResponse(BaseModel):
    history: List[Dict[str, Any]]
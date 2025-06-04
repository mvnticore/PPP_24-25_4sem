from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class TSPRequest(BaseModel):
    points: List[List[float]]

class TSPResponse(BaseModel):
    task_id: str

class WebSocketNotification(BaseModel):
    status: str
    task_id: str
    message: Optional[str] = None
    progress: Optional[int] = None
    path: Optional[List[int]] = None
    total_distance: Optional[float] = None
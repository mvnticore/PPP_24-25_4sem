from fastapi import FastAPI, Depends
from app.api.endpoints import task
from app.api import websocket
from app.db.session import engine, Base
from app.core.config import settings
from app.db.session import get_db
from app.core.security import router as auth_router, get_current_user
from app.schemas.task import UserCreate

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(task.router, prefix="/tasks", tags=["tasks"])
app.include_router(websocket.router, prefix="/ws", tags=["websocket"])

@app.get("/")
def read_root():
    return {"message": "TSP Solver API"}

@app.get("/protected")
def protected_route(user_id: str = Depends(get_current_user)):
    return {"message": f"Hello {user_id}, this is a protected route!"}
from sqlalchemy import Column, String, JSON, Float
from app.db.session import Base
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    email: str

class TSPSolution(Base):
    __tablename__ = "tsp_solutions"

    task_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    status = Column(String, default="PENDING")
    path = Column(JSON)
    total_distance = Column(Float)
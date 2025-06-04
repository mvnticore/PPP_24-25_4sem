from sqlalchemy.orm import Session
from app.models.task import TSPSolution
import uuid

def create_task(db: Session, user_id: str):
    task_id = str(uuid.uuid4())
    db_task = TSPSolution(
        task_id=task_id,
        user_id=user_id,
        status="PENDING"
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task_status(db: Session, task_id: str, status: str, path=None, total_distance=None):
    db_task = db.query(TSPSolution).filter(TSPSolution.task_id == task_id).first()
    if db_task:
        db_task.status = status
        if path is not None:
            db_task.path = path
        if total_distance is not None:
            db_task.total_distance = total_distance
        db.commit()
        db.refresh(db_task)
    return db_task
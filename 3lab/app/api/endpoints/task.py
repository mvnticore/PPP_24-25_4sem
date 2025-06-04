from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.task import TSPRequest, TSPResponse
from app.cruds.task import create_task
from app.celery.worker import solve_tsp_task
from app.db.session import get_db
from app.core.security import get_current_user

router = APIRouter()

@router.post("/solve-tsp", response_model=TSPResponse)
async def start_tsp_solution(
    request: TSPRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    task = create_task(db, user_id.id)
    solve_tsp_task.delay(
        task_id=task.task_id,
        user_id=user_id.id,
        points=request.points
    )
    return {"task_id": task.task_id}
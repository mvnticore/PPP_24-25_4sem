from celery import Celery
from app.core.config import settings
from app.services.tsp_solver import solve_tsp
from app.websocket.manager import ws_manager
from app.cruds.task import update_task_status
from app.db.session import SessionLocal

app = Celery(
    'tasks',
    broker=f'redislite://{settings.REDISLITE_PATH}',
    backend=f'redislite://{settings.REDISLITE_PATH}'
)


@app.task
def solve_tsp_task(task_id: str, user_id: str, points: list):
    db = SessionLocal()

    # Отправляем уведомление о начале
    ws_manager.push_notification(user_id, {
        "status": "STARTED",
        "task_id": task_id,
        "message": "Расчет маршрута начат"
    })
    update_task_status(db, task_id, "STARTED")

    for progress, path, distance in solve_tsp(points):
        if progress is not None:
            ws_manager.push_notification(user_id, {
                "status": "PROGRESS",
                "task_id": task_id,
                "progress": progress
            })

        if path is not None and distance is not None:
            update_task_status(db, task_id, "COMPLETED", path, distance)
            ws_manager.push_notification(user_id, {
                "status": "COMPLETED",
                "task_id": task_id,
                "path": path,
                "total_distance": distance
            })

    db.close()
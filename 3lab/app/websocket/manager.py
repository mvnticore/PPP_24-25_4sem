import json
import redis
from app.core.config import settings
from typing import Optional


class WebSocketManager:
    def __init__(self):
        self.redis = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=True
        )

    def push_notification(self, user_id: str, message: dict):
        self.redis.rpush(f"notifications:{user_id}", json.dumps(message))

    def pop_notification(self, user_id: str):
        if self.redis.llen(f"notifications:{user_id}") > 0:
            return json.loads(self.redis.lpop(f"notifications:{user_id}"))
        return None


ws_manager = WebSocketManager()
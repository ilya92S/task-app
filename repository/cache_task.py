import json
from dataclasses import dataclass

from redis import Redis

from schema.task import TaskSchema

@dataclass
class TaskCache:
    redis: Redis

    def get_tasks(self) -> list[TaskSchema] | TaskSchema:
        with self.redis as redis:
            task_json = redis.lrange("tasks", 0, -1)

            return [TaskSchema.model_validate(json.loads(task.decode('utf-8'))) for task in task_json]

    def set_tasks(self, tasks: list[TaskSchema]):
        tasks_json = [task.json() for task in tasks]
        with self.redis as redis:
            redis.lpush("tasks", *tasks_json)
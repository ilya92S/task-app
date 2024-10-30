import json
from dataclasses import dataclass

from redis import asyncio as Redis

from schema.task import TaskSchema

@dataclass
class TaskCache:
    redis: Redis

    async def get_tasks(self) -> list[TaskSchema] | TaskSchema:
        async with self.redis as redis:
            task_json = await redis.lrange("tasks", 0, -1)

            return [TaskSchema.model_validate(json.loads(task.decode('utf-8'))) for task in task_json]

    async def set_tasks(self, tasks: list[TaskSchema]):
        tasks_json = [task.model_dump_json() for task in tasks]
        async with self.redis as redis:
            await redis.lpush("tasks", *tasks_json)
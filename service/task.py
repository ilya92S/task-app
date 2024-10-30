from dataclasses import dataclass

from sqlalchemy.util import await_only

from exception import TaskNotFound
from repository import TaskRepository, TaskCache
from schema import TaskSchema, TaskCreateSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    async def get_task(self) -> list[TaskSchema]:
        if cache_tasks := await self.task_cache.get_tasks():
            return cache_tasks
        else:
            tasks = self.task_repository.get_all_tasks()
            tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
            await self.task_cache.set_tasks(tasks_schema)
            return tasks_schema

    async def create_task(self, body: TaskCreateSchema, user_id: int):
        task_id = await self.task_repository.create_task(task=body, user_id=user_id)
        task = await self.task_repository.get_task(task_id=task_id)
        return TaskSchema.model_validate(task)

    async def update_task_name(self, task_id: int, name: str, user_id: int) -> TaskSchema:
        task = await self.task_repository.get_user_task(task_id=task_id, user_id=user_id)
        if not task:
            raise TaskNotFound
        task = await self.task_repository.update_task_name(task_id=task_id, name=name)
        return TaskSchema.model_validate(task)

    async def delete_task(self, task_id: int, user_id: int) -> str:
        task = await self.task_repository.get_user_task(task_id=task_id, user_id=user_id)
        if not task:
            raise TaskNotFound
        return await self.task_repository.delete_task(task_id=task_id, user_id=user_id)

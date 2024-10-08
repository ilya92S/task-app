from dataclasses import dataclass

from exception import TaskNotFound
from repository import TaskRepository, TaskCache
from schema import TaskSchema, TaskCreateSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    def get_task(self) -> list[TaskSchema]:
        if tasks := self.task_cache.get_tasks():
            return tasks
        else:
            tasks = self.task_repository.get_all_tasks()
            print(tasks)
            tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
            print(tasks_schema)
            self.task_cache.set_tasks(tasks_schema)
            return tasks_schema

    def create_task(self, body: TaskCreateSchema, user_id: int):
        task_id = self.task_repository.create_task(task=body, user_id=user_id)
        task = self.task_repository.get_task(task_id=task_id)
        return TaskSchema.model_validate(task)

    def update_task_name(self, task_id: int, name: str, user_id: int) -> TaskSchema:
        task = self.task_repository.get_user_task(task_id=task_id, user_id=user_id)
        if not task:
            raise TaskNotFound
        task = self.task_repository.update_task_name(task_id=task_id, name=name)
        return TaskSchema.model_validate(task)

    def delete_task(self, task_id: int, user_id: int) -> str:
        task = self.task_repository.get_user_task(task_id=task_id, user_id=user_id)
        if not task:
            raise TaskNotFound
        return self.task_repository.delete_task(task_id=task_id, user_id=user_id)

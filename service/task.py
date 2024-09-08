from dataclasses import dataclass

from repository import TaskRepository, TaskCache
from schema import TaskSchema

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
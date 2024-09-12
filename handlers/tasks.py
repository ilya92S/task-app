from fastapi import APIRouter, Depends
from typing import Annotated

from dependency import get_task_service, get_tasks_repository
from repository import TaskRepository, TaskCache

from schema.task import TaskSchema
from service import TaskService

router = APIRouter(prefix="/task", tags=["task"])


@router.post("/drop-all")
async def drop_all_table(
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]
):

    task_repository.create_tasks_and_category()


@router.get("/all", response_model=list[TaskSchema])
async def get_task(
        task_service: Annotated[TaskService, Depends(get_task_service)]
):
    return task_service.get_task()

@router.post("/create-task")
async def create_task(
        task: TaskSchema,
        task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]
):

    task_id = task_repository.create_task(task)
    return task_id

@router.patch("/patch-task", response_model=TaskSchema)
async def patch_task(
        task_id: int,
        name: str,
        task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]
):
    return task_repository.update_task_name(task_id, name)


@router.delete("/delete-task")
async def delete_task(
        task_id: int,
        task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]
):
    task_repository.delete_task(task_id)
    return {"message": "task delete"}

@router.post("/create-data")
async def create_data(
        task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]
):
    task_repository.create_tasks_and_category()
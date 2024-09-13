from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from dependency import (
    get_task_service,
    get_tasks_repository,
    get_request_user_id
)
from exception import TaskNotFound
from repository import TaskRepository

from schema import TaskCreateSchema, TaskSchema
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

@router.post(
    "/create-task",
    response_model=TaskSchema
)
async def create_task(
        body: TaskCreateSchema,
        task_service: Annotated[TaskService, Depends(get_task_service)],
        user_id: int = Depends(get_request_user_id)
):
    task = task_service.create_task(body, user_id)
    return task

@router.patch("/patch-task", response_model=TaskSchema)
async def patch_task(
        task_id: int,
        name: str,
        task_service: Annotated[TaskService, Depends(get_task_service)],
        user_id: int = Depends(get_request_user_id)
):
    try:
        return task_service.update_task_name(task_id=task_id, name=name, user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )


@router.delete("/delete-task")
async def delete_task(
        task_id: int,
        task_service: Annotated[TaskService, Depends(get_task_service)],
        user_id: int = Depends(get_request_user_id)
) -> str:
    try:
        task_name = task_service.delete_task(task_id=task_id, user_id=user_id)
        return task_name
    except TaskNotFound as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )

@router.post("/create-data")
async def create_data(
        task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]
):
    task_repository.create_tasks_and_category()
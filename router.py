from fastapi import APIRouter
from typing import Annotated
from fastapi import Depends
from repository import TaskRepository
from schemes import STaskAdd, STask, STaskId

router = APIRouter(
    # prefix='/Tasks'
    tags=['mike']
)


@router.post('/task')
async def add_task(task: Annotated[STaskAdd, Depends()]) -> STaskId:
    task_id = await TaskRepository.add_one(task)
    return {"data": task_id}


# @app.get('/tasks')
# async def get_tasks():
#     task = Task(name="Buy groceries", description="Buy milk, eggs, and bread")
#     return ({"data": task}
@router.get('/tasks')
async def get_tasks() -> list[STask]:
    tasks = await TaskRepository.get_all()
    return tasks


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@router.get('/home')
async def home():
    return {"message": "Hello Home"}


from contextlib import asynccontextmanager

from fastapi import FastAPI
from database import create_tables, delete_tables
from router import router as tasks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print('database deleted')
    await create_tables()
    print('database created')
    yield
    print('lifespan')


app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)



# class Task(BaseModel):
#     name: str
#     description: str | None = None

# tasks = []





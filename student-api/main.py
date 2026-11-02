from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_tables
from routers.student import router as student_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(title="Student Management API", lifespan=lifespan)
app.include_router(student_router)


@app.get("/health")
def health():
    return {"status": "ok"}

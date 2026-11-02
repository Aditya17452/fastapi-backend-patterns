import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.dependencies import get_current_user
from database import get_db
from infrastructure.redis_client import cache_delete, cache_get, cache_set
from schemas.student import StudentCreate, StudentOut, StudentUpdate
from services import (
    create_student,
    delete_student,
    get_student_by_id,
    get_students,
    login_student,
    register_student,
    update_student,
)

router = APIRouter(tags=["students"])

CACHE_TTL_SECONDS = 60


def cache_key(student_id: int) -> str:
    return f"student:{student_id}"


@router.post("/student/register", response_model=StudentOut, status_code=201)
async def register_student_endpoint(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = register_student(db=db, student=student)
    if db_student is None:
        raise HTTPException(status_code=409, detail="Student already exists")
    return db_student


@router.post("/student/login")
async def login_student_endpoint(id: int, password: str, db: Session = Depends(get_db)):
    token = login_student(db=db, id=id, password=password)
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid student id or password")
    return token


@router.get("/students", response_model=list[StudentOut])
async def read_students(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_students(db=db)


@router.post("/students", response_model=StudentOut, status_code=201)
async def create_students(
    student: StudentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return create_student(db=db, student=student)


@router.get("/student/{id}", response_model=StudentOut)
async def read_student(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # Cache-aside: try Redis first, fall back to the database and populate the cache
    cached = await cache_get(cache_key(id))
    if cached:
        return json.loads(cached)

    db_student = get_student_by_id(student_id=id, db=db)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    data = StudentOut.model_validate(db_student).model_dump()
    await cache_set(cache_key(id), json.dumps(data), CACHE_TTL_SECONDS)
    return data


@router.put("/student/{id}", response_model=StudentOut)
async def update_student_endpoint(
    id: int, student: StudentUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    db_student = update_student(db=db, student_id=id, student=student)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    await cache_delete(cache_key(id))
    return db_student


@router.delete("/student/{id}", response_model=StudentOut)
async def delete_student_endpoint(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_student = delete_student(db=db, student_id=id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    await cache_delete(cache_key(id))
    return db_student

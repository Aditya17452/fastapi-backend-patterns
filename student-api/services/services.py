from sqlalchemy.orm import Session

from auth.hashing import hash_password, verify_password
from auth.jwt import create_access_token
from models.student import Student as StudentModel
from schemas.student import StudentCreate, StudentUpdate


def create_student(db: Session, student: StudentCreate):
    db_student = StudentModel(
        id=student.id,
        name=student.name,
        email=student.email,
        password_hash=hash_password(student.password),
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_students(db: Session):
    return db.query(StudentModel).all()


def get_student_by_id(student_id: int, db: Session):
    return db.query(StudentModel).filter(StudentModel.id == student_id).first()


def update_student(db: Session, student_id: int, student: StudentUpdate):
    st = get_student_by_id(student_id, db)
    if st is None:
        return None
    st.name = student.name
    st.email = student.email
    db.commit()
    db.refresh(st)
    return st


def delete_student(db: Session, student_id: int):
    st = get_student_by_id(student_id, db)
    if st is None:
        return None
    db.delete(st)
    db.commit()
    return st


def register_student(db: Session, student: StudentCreate):
    existing = db.query(StudentModel.id).filter(StudentModel.id == student.id).first()
    if existing:
        return None
    return create_student(db, student)


def login_student(db: Session, id: int, password: str):
    st = get_student_by_id(id, db)
    if st is None or not st.password_hash or not verify_password(password, st.password_hash):
        return None
    return {"access_token": create_access_token(student_id=st.id), "token_type": "bearer"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import services, schemas
from db import get_db
from models import User
from auth import get_current_user, get_admin_user

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/", response_model=list[schemas.Student])
def get_all_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.get_students(db)

@router.post("/", response_model=schemas.Student)
def create_new_student(
    std: schemas.StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    return services.create_student(db, std)

@router.put("/{id}", response_model=schemas.Student)
def update_student(
    id: int,
    std: schemas.StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    db_update = services.update_student(db, id, std)
    if not db_update:
        raise HTTPException(status_code=404, detail="Student Not Found")
    return db_update

@router.delete("/{id}", response_model=schemas.Student)
def delete_student(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    deleted = services.delete_student(db, id)
    if deleted:
        return deleted
    raise HTTPException(status_code=404, detail="Student Not Found")

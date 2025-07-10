from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import services, schemas
from db import get_db
from models import User
from auth import get_current_user, get_admin_user

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.get("/", response_model=list[schemas.Employee])
def get_all_employees(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.get_employees(db)

@router.post("/", response_model=schemas.Employee)
def create_new_employee(
    emp: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    return services.create_employee(db, emp)

@router.put("/{id}", response_model=schemas.Employee)
def update_employee(
    id: int,
    emp: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    db_update = services.update_employee(db, id, emp)
    if not db_update:
        raise HTTPException(status_code=404, detail="Employee Not Found")
    return db_update

@router.delete("/{id}", response_model=schemas.Employee)
def delete_employee(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    deleted = services.delete_employee(db, id)
    if deleted:
        return deleted
    raise HTTPException(status_code=404, detail="Employee Not Found")
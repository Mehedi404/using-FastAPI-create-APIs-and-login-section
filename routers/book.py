from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import services, schemas
from db import get_db
from models import User
from auth import get_current_user, get_admin_user

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=list[schemas.Book])
def get_all_books(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    return services.get_books(db)

@router.post("/", response_model=schemas.Book)
def create_new_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    return services.create_book(db, book)

@router.put("/{id}", response_model=schemas.Book)
def update_book(
    id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    db_update = services.update_book(db, id, book)
    if not db_update:
        raise HTTPException(status_code=404, detail="Book Not Found")
    return db_update

@router.delete("/{id}", response_model=schemas.Book)
def delete_book(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    deleted = services.delete_book(db, id)
    if deleted:
        return deleted
    raise HTTPException(status_code=404, detail="Book Not Found")


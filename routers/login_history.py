

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import LoginHistory, User
from auth import get_current_user

router = APIRouter(prefix="/login-history",tags=["Login History"])


@router.get("/")
def get_login_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    history = db.query(LoginHistory).filter(LoginHistory.user_id == current_user.id).all()
    return history

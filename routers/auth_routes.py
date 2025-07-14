from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
import uuid
from models import User
from config import VERIFY_EMAIL_URL, RESET_PASSWORD_URL
from utils.email import send_email_async
from security import pwd_context
import schemas
import services


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/resend-verification/")
async def resend_email(user: schemas.EmailRequest, db: Session = Depends(get_db)):
    user_obj = services.get_user_by_email(db, user.email)
    if not user_obj:
        raise HTTPException(404, "User not found")

    token = str(uuid.uuid4())
    user_obj.email_token = token
    db.commit()

    verify_url = f"{VERIFY_EMAIL_URL}/verify-email?token={token}"
    try:
        await send_email_async("Resend: Verify your email", user.email, f"Click here: {verify_url}")
        return {"message": "Verification email resent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send verification email: {e}")


@router.get("/verify-email/")
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email_token == token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    if user.is_verified:
        return {"message": "Email already verified"}

    user.is_verified = True
    user.email_token = None
    db.commit()
    return {"message": "Email verified successfully"}


@router.post("/forget-password/")
async def forget_password(data: schemas.EmailRequest, db: Session = Depends(get_db)):
    user = services.get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(404, "User not found")

    token = str(uuid.uuid4())
    user.email_token = token
    db.commit()

    reset_url = f"{RESET_PASSWORD_URL}?token={token}"

    await send_email_async("Reset your password", user.email, f"Reset link: {reset_url}")

    return {"message": "Reset link sent to email"}


@router.post("/reset-password/")
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email_token == token).first()
    if not user:
        raise HTTPException(400, "Invalid token")

    user.hashed_password = pwd_context.hash(new_password)
    user.email_token = None
    db.commit()

    return {"message": "Password updated successfully"}

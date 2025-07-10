import uuid
from sqlalchemy.orm import Session
from utils.email import send_email_async
from config import VERIFY_EMAIL_URL, RESET_PASSWORD_URL
from models import User
from config import VERIFY_EMAIL_URL
from schemas import UserCreate
from security import pwd_context  # make sure this is imported correctly
verify_url = f"{VERIFY_EMAIL_URL}?token={token}"

from config import RESET_PASSWORD_URL

reset_url = f"{RESET_PASSWORD_URL}?token={token}"

async def create_user(db: Session, user_data: UserCreate):
    # Generate email verification token
    token = str(uuid.uuid4())

    # Hash the user's password
    hashed_password = pwd_context.hash(user_data.password)

    # Create User object
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        is_admin=user_data.is_admin,
        email_token=token,
        is_verified=False
    )

    # Add to DB
    db.add(user)
    db.commit()
    db.refresh(user)

    # Build verification URL
    verify_url = f"{VERIFY_EMAIL_URL}?token={token}"
    body = f"Hi {user.username},\n\nPlease click the link below to verify your email:\n{verify_url}"

    # Send email
    await send_email_async("Verify your email", user.email, body)

    return user

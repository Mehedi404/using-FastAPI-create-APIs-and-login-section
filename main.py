from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import uuid
import models, schemas, services
from db import get_db, engine
from schemas import RefreshTokenRequest
from auth import get_current_user, get_admin_user
from config import VERIFY_EMAIL_URL, RESET_PASSWORD_URL
from utils.email import send_email_async
from models import User
from security import pwd_context
from config import VERIFY_EMAIL_URL, RESET_PASSWORD_URL
from fastapi import BackgroundTasks
from routers import auth_routes
from fastapi import FastAPI
from routers import book, employee, student, auth_routes, headers,login_history
from fastapi import Request
from routers import login_history

from models.login_history import LoginHistory
from fastapi.staticfiles import StaticFiles
from routers.file_routes import router as file_router




# Routers
from routers import book, employee, student


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/media", StaticFiles(directory="media"), name="media")

# Include Routers
app.include_router(book.router)
app.include_router(employee.router)
app.include_router(student.router)
app.include_router(auth_routes.router)
app.include_router(headers.router)
app.include_router(login_history.router)
app.include_router(file_router)


# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get current user from token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, services.SECRET_KEY, algorithms=[services.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = services.get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user


# ---------- Auth Routes ----------


@app.post("/signup", response_model=schemas.User)
async def signup(
    background_tasks: BackgroundTasks,  # ✅ This comes first
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    if services.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already taken")

    if services.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")


    new_user = services.create_user(db, user)

    verify_url = f"{VERIFY_EMAIL_URL}?token={new_user.email_token}"
    body = f"Hi {new_user.username},\n\nPlease verify your email: {verify_url}"

    background_tasks.add_task(send_email_async, "Verify your email", new_user.email, body)

    return new_user


@app.post("/token", summary="Login with username or email")
def login( request: Request,form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = services.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Please verify your email before logging in")

    ip_address = request.client.host
    user_agent = request.headers.get("user-agent")
    login_entry = LoginHistory(user_id=user.id, ip_address=ip_address, user_agent=user_agent)
    db.add(login_entry)
    db.commit()

    access_token = services.create_access_token(data={"sub": user.username})
    refresh_token = services.create_refresh_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# ---------- Protected Route ----------


@app.get("/secure-data/")
def secure_data(current_user: schemas.User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, you're authenticated!"}

@app.get("/admin-panel/")
def admin_data(user: models.User = Depends(get_admin_user)):
    return {"message": f"Welcome admin, {user.username}"}

@app.post("/refresh-token")
def refresh_token(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    refresh_token = data.refresh_token
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token missing")
    try:
        payload = services.decode_token(refresh_token)
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = services.get_user_by_username_or_email(db, username)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        new_access_token = services.create_access_token(data={"sub": user.username})
        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid or expired refresh token")





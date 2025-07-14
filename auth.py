from fastapi import Depends, HTTPException, status

from jose import JWTError, jwt
from sqlalchemy.orm import Session

from db import get_db

from models import User
from config import SECRET_KEY, ALGORITHM
from security import api_key_scheme



def get_current_user(token: str = Depends(api_key_scheme), db: Session = Depends(get_db)):
    print("-----------",token)
    if token.startswith("Bear "):
        token = token[5:]

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user



def get_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions (admin only).",
        )
    return current_user

# security.py
from fastapi.security import APIKeyHeader

api_key_scheme = APIKeyHeader(name="My-Header")


# security.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

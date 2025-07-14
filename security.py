# security.py
from fastapi.security import APIKeyHeader
from passlib.context import CryptContext


api_key_scheme = APIKeyHeader(name="My-Header")
custom_header = APIKeyHeader(name="My-Header2")




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

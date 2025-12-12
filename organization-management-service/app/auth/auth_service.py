# app/auth/auth_service.py
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv("JWT_SECRET", "defaultsecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd.hash(password)

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        return pwd.verify(plain, hashed)

    @staticmethod
    def create_access_token(data: dict, expires_hours: int = ACCESS_TOKEN_EXPIRE_HOURS) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(hours=expires_hours)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)

    @staticmethod
    def decode_token(token: str):
        try:
            payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None

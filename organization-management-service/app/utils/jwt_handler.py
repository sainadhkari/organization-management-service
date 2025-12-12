# app/utils/jwt_handler.py
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from app.auth.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")

def get_current_admin(token: str = Depends(oauth2_scheme)):
    return AuthService.decode_token(token)

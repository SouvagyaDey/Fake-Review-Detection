from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import secrets
from core.database import SessionLocal
from core.user import User
from core.auth import get_db

router = APIRouter(prefix="/users", tags=["Users"])


class CreateUserRequest(BaseModel):
    username: str


@router.post("")
def create_user(req: CreateUserRequest, db=Depends(get_db)):
    """Create a new user and get an API key"""
    existing = db.query(User).filter(User.username == req.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    api_key = secrets.token_hex(16)
    user = User(username=req.username, api_key=api_key, is_admin=False)
    db.add(user)
    db.commit()
    
    return {"username": req.username, "api_key": api_key}

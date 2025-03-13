import bcrypt
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from security import hash_password, verify_password, create_access_token
from datetime import timedelta


def create_user(db: Session, username: str, email: str, password: str, is_admin=False):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise ValueError("Username already exists")
    
    hashed_password = hash_password(password)  # Ensure you hash the password before saving
    new_user = User(username=username, email=email, hashed_password=hashed_password, is_admin=is_admin)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def generate_token(user):
    return create_access_token({"sub": user.username, "is_admin": user.is_admin}, timedelta(minutes=30))

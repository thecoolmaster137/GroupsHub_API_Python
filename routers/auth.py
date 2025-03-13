from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.user import UserCreate, UserLogin, UserResponse
from repositories.user_repository import create_user, authenticate_user, generate_token
from models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/auth/register-admin")
def register_admin(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_admin = create_user(db, user.username, user.email, user.password, is_admin=True)
        return {"message": "Admin registered successfully", "admin": new_admin.username}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    
@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return create_user(db, user.username, user.email, user.password, False)


@router.post("/signin")
def signin(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = generate_token(db_user)
    return {"access_token": token, "token_type": "bearer"}

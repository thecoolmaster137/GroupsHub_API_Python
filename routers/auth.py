from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.user import UserCreate, UserLogin, UserResponse
from repositories.user_repository import create_user, authenticate_user, generate_token
from models.user import User
from security import verify_password, create_access_token
from fastapi import Body

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register-admin")
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
def signin(request: UserLogin = Body(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": user.username, "is_admin": user.is_admin})
    return {"access_token": access_token, "token_type": "bearer"}  # Ensure token_type is included

@router.post("/test")
async def test_route(data: dict):
    print("Received data:", data)
    return {"message": "Received", "data": data}

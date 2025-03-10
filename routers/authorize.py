# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from database import get_db
# from schemas import UserLogin, Token
# from security.jwt_manager import JWTManager
# from repositories.admin_repository import AdminRepository

# router = APIRouter(prefix="/auth", tags=["Authentication"])

# @router.post("/", response_model=Token)
# def get_token(user: UserLogin, db: Session = Depends(get_db)):
#     user_data = AdminRepository.authenticate(db, user.username, user.password)
#     if not user_data:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     token = JWTManager.create_token(user_data)
#     return {"access_token": token, "token_type": "bearer"}

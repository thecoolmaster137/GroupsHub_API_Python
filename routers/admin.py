# from fastapi import APIRouter, Depends, HTTPException
# from typing import List
# from uuid import UUID
# from repositories.admin_repository import AdminRepository
# from schemas import AddAdminDto, AdminDto

# router = APIRouter(prefix="/api/admin", tags=["Admin"])

# @router.get("/", response_model=List[AdminDto])
# def get_all(admin_repo: AdminRepository = Depends()):
#     return admin_repo.get_all()

# @router.get("/{id}", response_model=AdminDto)
# def get_by_id(id: UUID, admin_repo: AdminRepository = Depends()):
#     admin = admin_repo.get_by_id(id)
#     if not admin:
#         raise HTTPException(status_code=404, detail="Admin not found")
#     return admin

# @router.get("/uName")
# def get_by_username(uName: str, passw: str, admin_repo: AdminRepository = Depends()):
#     admin = admin_repo.get_by_username(uName, passw)
#     if not admin:
#         raise HTTPException(status_code=400, detail="Invalid Credentials")
#     return admin

# @router.post("/", response_model=AdminDto)
# def add_user(admin_data: AddAdminDto, admin_repo: AdminRepository = Depends()):
#     admin = admin_repo.create_user(admin_data)
#     if not admin:
#         raise HTTPException(status_code=400, detail="Username already exists")
#     return admin

# @router.put("/{id}", response_model=AdminDto)
# def update_user(id: UUID, admin_data: AddAdminDto, admin_repo: AdminRepository = Depends()):
#     return admin_repo.update_user(id, admin_data)

# from sqlalchemy.orm import Session
# from models.admin import Admin
# from schemas.add_admin import AddAdmin
# from typing import List, Optional

# class AdminRepository:
#     def __init__(self, db: Session):
#         self.db = db
    
#     def get_all(self) -> List[Admin]:
#         return self.db.query(Admin).all()

#     def get_by_id(self, id: str) -> Optional[Admin]:
#         return self.db.query(Admin).filter(Admin.admin_id == id).first()
    
#     def create_user(self, add_admin_dto: AddAdmin) -> Optional[Admin]:
#         existing_admin = self.db.query(Admin).filter(Admin.username == add_admin_dto.username).first()
#         if not existing_admin:
#             new_admin = Admin(**add_admin_dto.model_dump())
#             self.db.add(new_admin)
#             self.db.commit()
#             self.db.refresh(new_admin)
#             return new_admin
#         return None

#     def delete_user(self, id: str) -> Optional[Admin]:
#         admin = self.db.query(Admin).filter(Admin.admin_id == id).first()
#         if admin:
#             self.db.delete(admin)
#             self.db.commit()
#         return admin

#     def update_user(self, id: str, add_admin_dto: AddAdmin) -> Optional[Admin]:
#         admin = self.db.query(Admin).filter(Admin.admin_id == id).first()
#         if admin:
#             for key, value in add_admin_dto.model_dump().items():
#                 setattr(admin, key, value)
#             self.db.commit()
#             self.db.refresh(admin)
#         return admin
    
#     def get_by_user_name(self, username: str, password: str) -> Optional[Admin]:
#         admin = self.db.query(Admin).filter(Admin.username == username).first()
#         return admin if admin and admin.password == password else None

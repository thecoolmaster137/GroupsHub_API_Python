from sqlalchemy.orm import Session
from psycopg2 import IntegrityError
from models.application import Application
from schemas.add_application import AddApplication as AddApplicationDto
from typing import List, Optional

class AppRepository:
    def __init__(self, db: Session):
        self.db = db

    # def add_app(self, add_app_dto: AddApplicationDto) -> Optional[Application]:
    #     existing_app = self.db.query(Application).filter(Application.app_name == add_app_dto.name).first()
    #     if not existing_app:
    #         new_app = Application(app_name=add_app_dto.name)
    #         self.db.add(new_app)
    #         self.db.commit()
    #         self.db.refresh(new_app)
    #         return new_app
    #     return None
    
    def add_app(self, add_app_dto: AddApplicationDto) -> Optional[dict]:
       """ Adds a new application if it doesn't already exist. """
       existing_app = self.db.query(Application).filter(Application.app_name == add_app_dto.name).first()
       if existing_app:
           return None  # Application already exists
       new_app = Application(app_name=add_app_dto.name)
       try:
           self.db.add(new_app)
           self.db.commit()
           self.db.refresh(new_app)
           return {"id": new_app.app_id, "name": new_app.app_name}
       except IntegrityError:
           self.db.rollback()
           return None  # Handle database error safely


    def delete_app(self, id: int) -> bool:
        app = self.db.query(Application).filter(Application.app_id == id).first()
        if app:
            self.db.delete(app)
            self.db.commit()
            return True
        return False

    def get_all(self) -> List[dict]:  # Return a list of dictionaries
        return [{"id": app.app_id, "name": app.app_name} for app in self.db.query(Application).all()]


    # def get_by_id(self, id: int) -> Optional[Application]:  # Removed `db` parameter
    #     return self.db.query(Application).filter(Application.app_id == id).first()

    def get_by_id(self, id: int) -> Optional[Application]:
        return self.db.query(Application).filter(Application.app_id == id).first()


    # def update_app(self, id: int, add_app_dto: AddApplicationDto) -> Optional[Application]:  # Removed `db` parameter
    #     app = self.db.query(Application).filter(Application.id == id).first()
    #     if app:
    #         app.app_name = add_app_dto.name
    #         self.db.commit()
    #         self.db.refresh(app)
    #         return app
    #     return None

    def update_app(self, id: int, application_data: AddApplicationDto) -> Optional[Application]:
        app = self.db.query(Application).filter(Application.app_id == id).first()
        if not app:
            return None

        app.app_name = application_data.name  # Use the correct model
        self.db.commit()
        self.db.refresh(app)
        return app



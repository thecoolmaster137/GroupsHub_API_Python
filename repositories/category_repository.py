from sqlalchemy.orm import Session
from models import Category
from schemas import CategoryDto
from typing import List, Optional

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_categories(self) -> List[Category]:
        return self.db.query(Category).all()

    def get_category_by_id(self, id: int) -> Optional[Category]:
        return self.db.query(Category).filter(Category.id == id).first()

    def add_category(self, category_dto: CategoryDto) -> Optional[Category]:
        existing_category = self.db.query(Category).filter(Category.category_name == category_dto.category_name).first()
        if not existing_category:
            new_category = Category(**category_dto.model_dump())
            self.db.add(new_category)
            self.db.commit()
            self.db.refresh(new_category)
            return new_category
        return None

    def update_category(self, id: int, category_dto: CategoryDto) -> Optional[Category]:
        category = self.db.query(Category).filter(Category.id == id).first()
        if category:
            for key, value in category_dto.model_dump().items():
                setattr(category, key, value)
            self.db.commit()
            self.db.refresh(category)
        return category

    def delete_category(self, id: int) -> bool:
        category = self.db.query(Category).filter(Category.id == id).first()
        if category:
            self.db.delete(category)
            self.db.commit()
            return True
        return False

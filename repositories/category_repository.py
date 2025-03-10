from sqlalchemy.orm import Session
from models.category import Category
from models.group import Group
from schemas.category import Category as CategoryDTO
from schemas.add_category import AddCategory
from schemas.group import Group as GroupDTO
from typing import List, Optional

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[CategoryDTO]:
        categories = self.db.query(Category).all()
        return [CategoryDTO(id=cat.cat_id, name=cat.cat_name) for cat in categories]

    def get_by_id(self, category_id: int) -> Optional[CategoryDTO]:
        category = self.db.query(Category).filter(Category.cat_id == category_id).first()
        if category:
            return CategoryDTO(id=category.cat_id, name=category.cat_name)
        return None

    def get_groups_by_category(self, category_id: int) -> List[GroupDTO]:
        groups = self.db.query(Group).filter(Group.cat_id == category_id).all()
        return [
            GroupDTO(
                group_id=g.group_id,
                group_name=g.group_name,
                group_link=g.group_link,
                group_image=g.group_image,
                cat_name=g.category.cat_name if g.category else "",
                cat_id=g.cat_id,
                country=g.country,
                language=g.language,
                group_desc=g.group_desc,
                group_rules=g.group_rules,
                tags=g.tags,
            )
            for g in groups
        ]

    def add_category(self, add_category_dto: AddCategory) -> Optional[CategoryDTO]:
        existing_category = self.db.query(Category).filter(Category.cat_name == add_category_dto.name).first()
        if existing_category:
            return None
        
        new_category = Category(cat_name=add_category_dto.name)
        self.db.add(new_category)
        self.db.commit()
        self.db.refresh(new_category)
        return CategoryDTO(id=new_category.cat_id, name=new_category.cat_name)

    def update_category(self, category_id: int, add_category_dto: AddCategory) -> Optional[CategoryDTO]:
        category = self.db.query(Category).filter(Category.cat_id == category_id).first()
        if not category:
            return None
        
        category.cat_name = add_category_dto.name
        self.db.commit()
        return CategoryDTO(id=category.cat_id, name=category.cat_name)

    def delete_category(self, category_id: int) -> bool:
        category = self.db.query(Category).filter(Category.cat_id == category_id).first()
        if not category:
            return False
        
        self.db.delete(category)
        self.db.commit()
        return True

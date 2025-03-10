from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Groups, Category, Application
from schemas import GroupDto, AddGroupDto
from typing import List, Optional

class GroupRepository:
    def __init__(self, db: Session, get_groups):
        self.db = db
        self.get_groups = get_groups

    def exist_group(self, group_link: str) -> Optional[GroupDto]:
        group = self.db.query(Groups).filter(Groups.groupLink == group_link).first()
        if group:
            category = self.db.query(Category).filter(Category.catId == group.catId).first()
            return GroupDto(
                groupId=group.groupId,
                groupName=group.groupName,
                GroupImage=group.GroupImage,
                catName=category.catName,
                groupDesc=group.groupDesc,
                groupLink=group.groupLink,
                groupRules=group.groupRules,
                country=group.country,
                Language=group.Language,
                tags=group.tags
            )
        return None

    def get_all(self):
        return self.db.query(Groups).all()

    def get_by_id(self, group_id: int) -> Optional[GroupDto]:
        group = self.db.query(Groups).filter(Groups.groupId == group_id).first()
        if group:
            category = self.db.query(Category).filter(Category.catId == group.catId).first()
            return GroupDto(
                groupId=group.groupId,
                groupName=group.groupName,
                GroupImage=group.GroupImage,
                catName=category.catName,
                groupDesc=group.groupDesc,
                groupLink=group.groupLink,
                groupRules=group.groupRules,
                country=group.country,
                Language=group.Language,
                tags=group.tags
            )
        return None

    def get_groups(self) -> List[GroupDto]:
        groups = self.db.query(Groups).order_by(Groups.groupId).all()
        return self.get_groups.list_group_dto(groups)

    def get_group_by_category(self, cat_id: int) -> List[GroupDto]:
        groups = self.db.query(Groups).filter(Groups.catId == cat_id).all()
        return self.get_groups.list_group_dto(groups)

    def add_group(self, cat_id: int, app_id: int, add_group_dto: AddGroupDto) -> Optional[GroupDto]:
        if self.exist_group(add_group_dto.groupLink):
            raise HTTPException(status_code=400, detail="Group already exists")
        
        group = Groups(
            catId=cat_id,
            appId=app_id,
            groupName=add_group_dto.groupName,
            GroupImage=add_group_dto.GroupImage,
            groupLink=add_group_dto.groupLink,
            groupDesc=add_group_dto.groupDesc,
            groupRules=add_group_dto.groupRules,
            country=add_group_dto.country,
            Language=add_group_dto.Language,
            tags=add_group_dto.tags
        )
        self.db.add(group)
        self.db.commit()
        self.db.refresh(group)
        return self.get_by_id(group.groupId)

    def update_group(self, group_id: int, cat_id: int, app_id: int, add_group_dto: AddGroupDto) -> Optional[GroupDto]:
        group = self.db.query(Groups).filter(Groups.groupId == group_id).first()
        if not group:
            return None
        
        group.catId = cat_id
        group.appId = app_id
        group.groupLink = add_group_dto.groupLink
        group.groupDesc = add_group_dto.groupDesc
        group.groupRules = add_group_dto.groupRules
        group.country = add_group_dto.country
        group.Language = add_group_dto.Language
        group.tags = add_group_dto.tags
        
        self.db.commit()
        self.db.refresh(group)
        return self.get_by_id(group.groupId)

    def delete_group(self, group_id: int) -> bool:
        group = self.db.query(Groups).filter(Groups.groupId == group_id).first()
        if not group:
            return False
        
        self.db.delete(group)
        self.db.commit()
        return True

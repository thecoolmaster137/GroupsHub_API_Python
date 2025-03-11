from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from models.group import Group
from models.category import Category
from schemas.add_group import AddGroup
from schemas.group import Group as GroupSchema
from typing import List, Optional

def get_groups(db: Session) -> List[GroupSchema]:
    """Retrieve all groups from the database and include category name."""
    results = (
        db.query(Group, Category.cat_name)  # Fetch group and category name
        .outerjoin(Category, Group.cat_id == Category.cat_id)
        .all()
    )

    # Convert query results into list of GroupSchema objects
    return [
        GroupSchema(
            **group.__dict__,
            cat_name=cat_name  # Extract category name from tuple
        )
        for group, cat_name in results
    ]

def get_group_by_id(db: Session, group_id: int) -> Optional[GroupSchema]:
    """Retrieve a single group by its ID and include category name."""
    result = (
        db.query(Group, Category.cat_name)
        .outerjoin(Category, Group.cat_id == Category.cat_id)
        .filter(Group.group_id == group_id)
        .first()
    )

    if result:
        group, cat_name = result
        return GroupSchema(
            **group.__dict__,
            cat_name=cat_name
        )
    
    return None


def get_group_by_link(db: Session, group_link: str) -> Group:
    """Check if a group with the given link already exists."""
    return db.query(Group).filter(Group.group_link == group_link).first()

def add_group(db: Session, group_data: AddGroup) -> Group:
    """Add a new group to the database."""
    new_group = Group(
        group_name="",  # Will be updated after scraping
        group_link=group_data.group_link,
        country=group_data.country,
        language=group_data.language,
        group_desc=group_data.group_desc,
        group_rules=group_data.group_rules,
        tags=group_data.tags,
        app_id=group_data.app_id,
        cat_id=group_data.cat_id,
        group_image="",  # Will be updated after scraping
    )
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group

def delete_group(db: Session, group_id: int) -> bool:
    """Delete a group by its ID."""
    group = db.query(Group).filter(Group.group_id == group_id).first()
    if group:
        db.delete(group)
        db.commit()
        return True
    return False


def update_group(db: Session, group_id: int, group_data: AddGroup) -> Optional[dict]:
    """Update an existing group."""
    group = db.query(Group).filter(Group.group_id == group_id).first()

    if group:
        # Update group details
        group.group_link = group_data.group_link
        group.country = group_data.country
        group.language = group_data.language
        group.group_desc = group_data.group_desc
        group.group_rules = group_data.group_rules
        group.tags = group_data.tags
        group.cat_id = group_data.cat_id  # Ensure category is updated

        db.commit()
        db.refresh(group)

        # Fetch category name
        cat_name = group.category.cat_name if group.category else None  # Assuming a relationship exists

        # Return a dictionary instead of a Group instance
        return {
            "group_id": group.group_id,
            "group_name": group.group_name,
            "group_link": group.group_link,
            "group_image": group.group_image,
            "cat_id": group.cat_id,
            "cat_name": cat_name,  # Include category name
            "country": group.country,
            "language": group.language,
            "group_desc": group.group_desc,
            "group_rules": group.group_rules,
            "tags": group.tags,
            "message": "Group updated successfully"
        }

    return None



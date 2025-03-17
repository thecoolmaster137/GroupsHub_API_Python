from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from repositories.group_repository import (
    get_groups,
    get_group_by_id,
    add_group,
    delete_group,
    update_group,
    search_groups
)
from schemas.add_group import AddGroup
from schemas.group import Group
from repositories.group_repository import add_group, get_group_by_link
from services.group_scraper import get_group_image_and_name
from models.category import Category  # Import Category model
from validators import url as validate_url
from typing import List, Optional
from security import get_current_user

router = APIRouter(prefix="/groups", tags=["Groups"])

@router.get("/", response_model=List[Group])
def fetch_groups(db: Session = Depends(get_db)):
    """Retrieve all groups."""
    return get_groups(db)

@router.get("/{group_id}", response_model=Group)
def fetch_group(group_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific group by ID."""
    group = get_group_by_id(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@router.post("/", response_model=Group)
def create_group(
    group_data: AddGroup, 
    db: Session = Depends(get_db)
):
    """Create a new group with validation and web scraping for details."""
    
    # Validate the group link
    if not validate_url(group_data.group_link):
        raise HTTPException(status_code=400, detail="Invalid group link provided.")
    
    # Check if the group already exists
    existing_group = get_group_by_link(db, group_data.group_link)
    if existing_group:
        raise HTTPException(status_code=400, detail="Group already exists.")
    
    # Scrape group details
    group_info = get_group_image_and_name(group_data.group_link)
    
    if not group_info:
        raise HTTPException(status_code=500, detail="Failed to scrape group details. Network issue or invalid link.")
    
    # Add the group to the database
    new_group = add_group(db, group_data)
    new_group.group_name = group_info["group_name"]
    new_group.group_image = group_info["group_image"]
    
    db.commit()
    db.refresh(new_group)
    
    return new_group

# Apply authentication **only to this route**
@router.put("/{group_id}", response_model=dict)
def modify_group(
    group_id: int, 
    group_data: AddGroup, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Require authentication
):
    """Update an existing group."""
    
    if not current_user.get("is_admin"):  # Only allow admins
        raise HTTPException(status_code=403, detail="Admin access required")

    updated_group = update_group(db, group_id, group_data)
    if not updated_group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    return updated_group

# Apply authentication **only to this route**
@router.delete("/{group_id}", response_model=dict)
def remove_group(
    group_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Require authentication
):
    """Delete a group by ID."""
    
    if not current_user.get("is_admin"):  # Only allow admins
        raise HTTPException(status_code=403, detail="Admin access required")

    if delete_group(db, group_id):
        return {"message": "Group deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Group not found")

@router.get("/search/", response_model=List[Group])
def search_groups_endpoint(
    cat_id: Optional[int] = None,
    country: Optional[str] = None,
    language: Optional[str] = None,
    app_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Search groups by category ID, country, language, and application ID.
    - If no filters are provided, returns all groups.
    - Supports any combination of filters.
    """
    return search_groups(db, cat_id, country, language, app_id)

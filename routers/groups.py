from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from repositories.group_repository import (
    get_groups,
    get_group_by_id,
    add_group,
    delete_group,
    update_group
)
from schemas.add_group import AddGroup
from schemas.group import Group
from repositories.group_repository import add_group, get_group_by_link
from services.group_scraper import get_group_image_and_name
from models.category import Category  # Import Category model
from validators import url as validate_url
from typing import List

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
def create_group(group_data: AddGroup, db: Session = Depends(get_db)):
    """Create a new group with validation and web scraping for details."""
    
    # Validate the group link
    if not validate_url(group_data.group_link):
        raise HTTPException(status_code=400, detail="Invalid group link provided.")
    
    # Step 2: Check if the group already exists in the database
    existing_group = get_group_by_link(db, group_data.group_link)
    if existing_group:
        raise HTTPException(status_code=400, detail="Group already exists.")
    
    # Step 3: Scrape group details
    group_info = get_group_image_and_name(group_data.group_link)
    
    if not group_info:
        raise HTTPException(status_code=500, detail="Failed to scrape group details. Network issue or invalid link.")
    
    # Step 4: Add the group to the database
    new_group = add_group(db, group_data)
    new_group.group_name = group_info["group_name"]
    new_group.group_image = group_info["group_image"]
    
    db.commit()
    db.refresh(new_group)
    
    return new_group
    

@router.put("/{group_id}", response_model=dict)
def modify_group(group_id: int, group_data: AddGroup, db: Session = Depends(get_db)):
    """Update an existing group."""
    updated_group = update_group(db, group_id, group_data)
    if not updated_group:
        raise HTTPException(status_code=404, detail="Group not found")
    return updated_group


@router.delete("/{group_id}", response_model=dict)
def remove_group(group_id: int, db: Session = Depends(get_db)):
    """Delete a group by ID."""
    if delete_group(db, group_id):
        return {"message": "Group deleted successfully"}
    raise HTTPException(status_code=404, detail="Group not found")

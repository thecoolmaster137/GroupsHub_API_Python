from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from repositories.category_repository import CategoryRepository
from schemas.add_category import AddCategory
from schemas.category import Category as CategorySchema
from security import get_current_user
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=list[CategorySchema])
def get_all_categories(db: Session = Depends(get_db)):
    categories = CategoryRepository(db).get_all()
    return categories

@router.get("/{id}", response_model=CategorySchema)
def get_category_by_id(id: int, db: Session = Depends(get_db)):
    category = CategoryRepository(db).get_by_id(id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/{id}/groups")
def get_groups_by_category(id: int, db: Session = Depends(get_db)):
    groups = CategoryRepository(db).get_groups_by_category(id)
    return groups

# Apply authentication **only to this route**
@router.post("/", response_model=CategorySchema)
def add_category(
    category_data: AddCategory, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Only this route needs auth
):
    print("Current User Data:", current_user)  # Debugging
    
    if not current_user.get("is_admin"):  # Only allow admins
        raise HTTPException(status_code=403, detail="Admin access required")
    
    new_category = CategoryRepository(db).add_category(category_data)
    return CategorySchema(id=new_category.id, name=new_category.name)

@router.put("/{id}", response_model=CategorySchema)
def update_category(id: int, category_data: AddCategory, db: Session = Depends(get_db)):
    updated_category = CategoryRepository(db).update_category(id, category_data)
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category

@router.delete("/{id}")
def delete_category(id: int, db: Session = Depends(get_db)):
    deleted = CategoryRepository(db).delete_category(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.add_application import AddApplication as ApplicationCreate
from schemas.application import Application as ApplicationResponse
from repositories.app_repository import AppRepository

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.get("/", response_model=list[ApplicationResponse])
def get_all(db: Session = Depends(get_db)):
    repo = AppRepository(db)
    return repo.get_all()


@router.get("/{id}", response_model=ApplicationResponse)
def get_by_id(id: int, db: Session = Depends(get_db)):
    repo = AppRepository(db)
    app = repo.get_by_id(id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    # Convert SQLAlchemy model to match Pydantic schema
    return {"id": app.app_id, "name": app.app_name}


@router.post("/", response_model=ApplicationResponse)
def add_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    repo = AppRepository(db)
    return repo.add_app(application)

@router.put("/{id}", response_model=ApplicationResponse)
def update_application(id: int, application: ApplicationCreate, db: Session = Depends(get_db)):
    repo = AppRepository(db)
    updated_app = repo.update_app(id, application)
    if not updated_app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return {"id": updated_app.app_id, "name": updated_app.app_name}

@router.delete("/{id}")
def delete_application(id: int, db: Session = Depends(get_db)):
    repo = AppRepository(db)
    if not repo.delete_app(id):
        raise HTTPException(status_code=404, detail="Application not found")
    return {"message": "Application deleted successfully"}

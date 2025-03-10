from fastapi import APIRouter

router = APIRouter()

@router.get("/groups")
def get_groups():
    return {"message": "List of groups"}

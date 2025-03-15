from fastapi import APIRouter, HTTPException
from repositories.countries_repository import get_all_countries, get_languages_by_country

router = APIRouter(prefix="/countries", tags=["Countries"])


@router.get("/", summary="Get all countries")
def get_countries():
    try:
        return get_all_countries()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/languages/{country_name}", summary="Get languages by country")
def get_languages(country_name: str):
    try:
        result = get_languages_by_country(country_name)
        if result:
            return result
        raise HTTPException(status_code=404, detail="Country not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

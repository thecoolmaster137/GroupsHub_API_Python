import json
from pathlib import Path

COUNTRIES_FILE = Path("src/country-by-languages.json")

def load_countries():
    """Load countries data from the JSON file."""
    if not COUNTRIES_FILE.exists():
        raise FileNotFoundError("countries.json file not found in src directory")
    
    with open(COUNTRIES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def get_all_countries():
    """Get a list of all countries."""
    countries_data = load_countries()
    return [{"country": item["country"]} for item in countries_data]

def get_languages_by_country(country_name: str):
    """Get languages for a specific country."""
    countries_data = load_countries()
    for item in countries_data:
        if item["country"].lower() == country_name.lower():
            return {"country": item["country"], "languages": item["languages"]}
    return None

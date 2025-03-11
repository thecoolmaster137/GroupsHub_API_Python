import requests
from bs4 import BeautifulSoup

def get_group_image_and_name(url: str):
    """Scrape group name and image from the given URL."""
    try:
        response = requests.get(url, timeout=10)  # 10-second timeout for reliability
        if response.status_code != 200:
            return None  # Request failed, return None
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        group_name = soup.select_one("#main_block h3")
        group_image = soup.select_one("#action-icon span img")

        if group_name and group_image:
            return {
                "group_name": group_name.text.strip(),
                "group_image": group_image["src"]
            }
    except requests.RequestException as e:
        print(f"Scraping Error: {e}")
    
    return None


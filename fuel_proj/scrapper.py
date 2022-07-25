import requests
import json

URL = "https://api.wog.ua/fuel_stations"

coordinates = {
    "longitude":26.23724,
    "latitude":50.612459
    }

def scraper(url):
    page = requests.get(url)
    with open ("file_json.txt", "w", encoding="utf8") as f:
        json.dump(page.text, f, indent=6)

    print(page.text)

scraper(URL)
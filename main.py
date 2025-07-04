import json
from scraper_categories import extract_categories
from scraper_category_page import extract_category_text
from scraper_lessons import extract_lesson_items

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from scraper_registrations import extract_registrations
from tools import normalize_url
import sys

# Setup console output
sys.stdout.reconfigure(encoding="utf-8")
# === Setup Selenium ===
chromedriver_path = "chromedriver.exe"

chrome_options = Options()
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# === Final output ===
site_data = {"categories": []}

try:
    # Step 1: Get all homepage categories
    categories = extract_categories(driver)

    for category in categories:
        full_url = normalize_url(category["link"])
        print(f"\n📂 Processing category: {category['title']}")

        description = extract_category_text(driver, full_url)

        # Try lessons first
        lessons = extract_lesson_items(driver, full_url)

        # If no lessons found, try registrations table
        registrations = []
        if not lessons:
            registrations = extract_registrations(driver, full_url)

        category_obj = {
            "name": category["title"],
            "img": category["bg_image"],
            "link": category["link"],
            "description": description,
            "lessons": (
                [
                    {
                        "name": lesson["title"],
                        "img": lesson["image"],
                        "link": lesson["link"],
                    }
                    for lesson in lessons
                ]
                if lessons
                else []
            ),
            "registrations": registrations if registrations else [],
        }

        site_data["categories"].append(category_obj)

    # Step 5: Save to JSON file
    with open("site_data.json", "w", encoding="utf-8") as f:
        json.dump(site_data, f, ensure_ascii=False, indent=2)

    print("\n✅ Data saved to site_data.json")

finally:
    driver.quit()

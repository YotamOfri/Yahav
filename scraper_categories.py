from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def extract_categories(driver, wait_time: int = 20):
    """
    Given a Selenium driver, loads the homepage and extracts all category blocks.
    Returns a list of dictionaries with title, link, bg_image, and icon_image.
    """
    wait = WebDriverWait(driver, wait_time)

    url = "https://www.pnay-b-y.org.il/index.php"
    driver.get(url)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inner")))
    time.sleep(2)  # Allow JS to load

    soup = BeautifulSoup(driver.page_source, "html.parser")
    categories = []

    for a_tag in soup.select("div.inner a.col"):
        href = a_tag.get("href", "").strip()
        full_link = (
            f"https://www.pnay-b-y.org.il{href}" if href.startswith("/") else href
        )

        # Background image
        bg_div = a_tag.select_one(".bg")
        bg_style = bg_div.get("style", "") if bg_div else ""
        bg_url = ""
        if "url(" in bg_style:
            bg_url = bg_style.split("url(")[1].split(")")[0].strip('"').strip()

        # Icon image
        img_tag = a_tag.select_one("img")
        img_url = img_tag.get("src", "") if img_tag else ""

        # Title
        title_tag = a_tag.select_one("h3")
        title = title_tag.get_text(strip=True) if title_tag else ""

        categories.append(
            {
                "title": title,
                "link": full_link,
                "bg_image": bg_url,
                "icon_image": img_url,
            }
        )

    print(f"✅ Extracted {len(categories)} categories.")
    return categories

from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


def extract_lesson_items(driver, category_url: str, wait_time: int = 20):
    """
    From a category page, extract lesson items (image, title, link).
    """
    wait = WebDriverWait(driver, wait_time)
    driver.get(category_url)

    try:
        # Wait for EITHER lessons container OR registration table to appear
        wait.until(
            EC.any_of(
                EC.presence_of_element_located((By.CLASS_NAME, "events_container")),
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "as-hobbies-list__table")
                ),
            )
        )
    except:
        # Timeout reached — no lessons or table found — just continue
        return []

    soup = BeautifulSoup(driver.page_source, "html.parser")
    lesson_cols = soup.select("div.events_container div.lesson div.inner div.col")
    if not lesson_cols:
        return []

    items = []

    for col in lesson_cols:
        # Image from .img_col .bg style
        bg_div = col.select_one(".img_col .bg")
        bg_style = bg_div.get("style", "") if bg_div else ""
        image_url = ""
        if "url(" in bg_style:
            image_url = bg_style.split("url(")[1].split(")")[0].strip('"').strip()

        # Title
        title_tag = col.select_one("h3") or col.select_one(".text h4")
        title = title_tag.get_text(strip=True) if title_tag else ""

        # Link
        a_tag = col.select_one(".text a")
        href = a_tag.get("href", "").strip() if a_tag else ""
        full_link = (
            f"https://www.pnay-b-y.org.il/{href}"
            if href and not href.startswith("http")
            else href
        )

        items.append(
            {
                "title": title,
                "image": image_url,
                "link": full_link,
            }
        )

    return items

from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


def extract_category_text(driver, category_url: str, wait_time: int = 20):
    """
    Extract all visible text inside div.right_center on a category page.
    Returns empty string if fails or div not found.
    """
    wait = WebDriverWait(driver, wait_time)

    try:
        driver.get(category_url)
    except WebDriverException as e:
        print(f"❌ Failed to load URL: {category_url} — {e}")
        return ""

    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "right_center")))
    except TimeoutException:
        print(f"⚠️ Timeout waiting for div.right_center at: {category_url}")
        return ""

    # Parse page content
    soup = BeautifulSoup(driver.page_source, "html.parser")
    right_center_div = soup.select_one("div.right_center")

    if not right_center_div:
        print(f"⚠️ No div.right_center found at: {category_url}")
        return ""

    # Get all visible text, joined by newlines, stripped
    text = right_center_div.get_text(separator="\n", strip=True)
    return text

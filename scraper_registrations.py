from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


def extract_registrations(driver, category_url: str, wait_time: int = 20):
    wait = WebDriverWait(driver, wait_time)
    driver.get(category_url)
    # Wait for either lessons container OR table
    try:
        wait.until(
            EC.any_of(
                EC.presence_of_element_located((By.CLASS_NAME, "events_container")),
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "as-hobbies-list__table")
                ),
            )
        )
    except:
        time.sleep(1)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    registrations = []

    table = soup.select_one("table.as-hobbies-list__table")
    if not table:
        return registrations  # empty list if no table found

    rows = table.select("tbody tr")
    for row in rows:
        cols = row.select("td")
        if len(cols) < 3:
            continue
        name = cols[0].get_text(strip=True)
        dates = cols[1].get_text(strip=True)
        a_tag = cols[2].select_one("a")
        href = a_tag.get("href", "") if a_tag else ""
        full_link = (
            f"https://www.pnay-b-y.org.il/{href}"
            if href and not href.startswith("http")
            else href
        )

        registrations.append({"name": name, "dates": dates, "link": full_link})

    return registrations

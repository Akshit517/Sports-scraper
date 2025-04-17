
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def start(player_search_name):
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        try:
            driver.get(
                "https://www.howstat.com/Cricket/Statistics/Players/PlayerMenu.asp")
            search_input = driver.find_element(By.ID, "txtPlayer")

            search_input.send_keys(player_search_name)
            search_input.send_keys(Keys.RETURN)
            time.sleep(2)

            player_search_name = driver.find_elements(
                By.CLASS_NAME, "LinkTable")
            player_search_name[0].click()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            soup = BeautifulSoup(driver.page_source, "html.parser")

            full_html = driver.page_source
            # print(soup)

            data = {}
            for row in soup.find_all("td", class_="FieldName2"):
                key = row.get_text(strip=True).replace("\xa0", " ")
                value_td = row.find_next_sibling("td")
                value = value_td.get_text(strip=True) if value_td else ""
                data[key.rstrip(":")] = value

            for k, v in data.items():
                print(f"{k}:{v}")

        finally:
            driver.quit()

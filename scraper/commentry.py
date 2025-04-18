from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os


class Commentary:
    def __init__(self, url, cooldown_time):
        self.options = Options()
        self.options.add_argument("--headless")
        self.url = f"https://www.cricbuzz.com/live-cricket-scores/{url}"
        self.code = url
        self.cooldown_time = cooldown_time

        if not os.path.exists("data"):
            os.makedirs("data")

    def get_commentary(self):
        driver = webdriver.Chrome(service=Service(), options=self.options)
        driver.get(self.url)

        try:
            commentary_tab = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Commentary"))
            )
            commentary_tab.click()
        except Exception as e:
            print("Couldn't click Commentary tab:", e)
            driver.quit()
            exit()

        while True:
            try:
                load_more_btn = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.ID, "full_commentary_btn"))
                )
                driver.execute_script("arguments[0].click();", load_more_btn)
                time.sleep(1.5)
            except:
                break

        commentary_blocks = driver.find_elements(
            By.CSS_SELECTOR, "div[id^='comm_']")

        # print(f"\nTotal balls found: {len(commentary_blocks)}\n")
        data = []
        for block in commentary_blocks:
            try:
                over = block.find_element(
                    By.CLASS_NAME, "cb-ovr-num").text.strip()
                text = block.find_element(
                    By.CLASS_NAME, "cb-com-ln").text.strip()
                data.append([over, text])
            except:

                continue

        filename = f"data/{self.code}.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Ball", "Commentary"])
            writer.writerows(data)

        driver.quit()
        print(f"Commentary data saved to {filename}.")

    def start_scraping(self):
        while True:
            print(f"Starting new scrape for {self.code}...")
            self.get_commentary()
            print(
                f"Waiting for {self.cooldown_time} seconds before next scrape.")
            time.sleep(self.cooldown_time)

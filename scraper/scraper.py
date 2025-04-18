import requests
from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scraper:
    def __init__(self, player_name):
        self.driver = None
        self.player_name = player_name
        self.base_url = "https://www.howstat.com"

    def get_player_id(self):
        url = self.driver.current_url
        if "PlayerID=" in url:
            return url.split("PlayerID=")[1]
        return None

    def get_player_info(self, soup):
        data = {}
        for row in soup.find_all("td", class_="FieldName2"):
            key = row.get_text(strip=True).replace("\xa0", " ")
            value_td = row.find_next_sibling("td")
            value = value_td.get_text(strip=True) if value_td else ""
            data[key.rstrip(":")] = value
            # print(f"{key}:{value}")

        return data

        # for k, v in data.items():
        #    print(f"{k}:{v}")

    def source_table_data(self, soup):
        tables = soup.find_all("table", class_="BorderedBox3")
        all_stats = []
        for table in tables:
            stats = self.extract_table_data(table)
            all_stats.append(stats)
        formats = ["Tests", "ODIs", "T20s", "Overall", "IPL"]
        for index, stats in enumerate(all_stats):
            if index < 6:
                stats["Format"] = formats[index]

        # print(all_stats)  # uncomment to debug

        json_output = json.dumps(all_stats, indent=4)
        #with open("player_stats.json", "w") as f:
         #   f.write(json_output)
        return json_output

    def extract_table_data(self, table):
        stats = {}
        rows = table.find_all("tr")
        current_section = None

        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 2:
                key_span = cols[0].find("span", class_="FieldName2")
                value_td = cols[1].text.strip()
                if key_span:
                    key = key_span.text.strip().replace(":", "")
                    stats[key] = value_td
            elif len(cols) == 1 and "background-color" in str(cols[0].get("style", "")):
                # Category header
                current_section = cols[0].text.strip()
                stats[current_section] = {}
            elif len(cols) == 2 and current_section:
                key_span = cols[0].find("span", class_="FieldName2")
                value_td = cols[1].text.strip()
                if key_span:
                    key = key_span.text.strip().replace(":", "")
                    stats[current_section][key] = value_td

        return stats

    def start(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

        try:
            self.driver.get(
                "https://www.howstat.com/Cricket/Statistics/Players/PlayerMenu.asp")
            search_input = self.driver.find_element(By.ID, "txtPlayer")
            search_input.send_keys(self.player_name)
            search_input.send_keys(Keys.RETURN)
            time.sleep(2)

            player_search_name = self.driver.find_elements(
                By.CLASS_NAME, "LinkTable")
            player_search_name[0].click()

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            # self.get_player_id()
            info =self.get_player_info(soup)
            stats =self.source_table_data(soup)
            return json.dumps({
    "info": info,
    "stats": json.loads(stats)
}, indent=4)

        finally:
            self.driver.quit()

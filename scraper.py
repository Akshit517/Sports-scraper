# # scraper.py
# from pathway import pw
# from pathway.io.python import ConnectorSubject
# from parsers.espn_cricket_parser import ESPNLiveCricketScoreParser 
# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# import time
# from datetime import datetime
# from typing import List
# from config import Config

# class CricketMatchSubject(ConnectorSubject):
#     def __init__(self, refresh_interval: int = Config.REFRESH_INTERVAL) -> None:
#         super().__init__()
#         self.refresh_interval = refresh_interval
#         self.driver = self._init_selenium()
#         self.parser = ESPNLiveCricketScoreParser()
#         self.url = "https://www.espncricinfo.com/live-cricket-score"
#         self.max_retries = 3

#     def _init_selenium(self):
#         options = Options()
#         options.add_argument("--headless")
#         service = Service(executable_path="/usr/local/bin/geckodriver")
#         return webdriver.Firefox(service=service, options=options)

#     def run(self) -> None:
#         retry_count = 0
#         while True:
#             try:
#                 self._scrape_and_emit()
#                 retry_count = 0  # Reset retry counter after success
#                 time.sleep(self.refresh_interval)
#             except Exception as e:
#                 print(f"Error in scraper: {str(e)}")
#                 retry_count += 1
#                 if retry_count >= self.max_retries:
#                     print("Max retries reached, restarting driver...")
#                     self.driver.quit()
#                     self.driver = self._init_selenium()
#                     retry_count = 0
#                 time.sleep(5)  # Wait before retry

#     def _scrape_and_emit(self):
#         try:
#             self.driver.get(self.url)
#             WebDriverWait(self.driver, 10).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, "div.ds-px-4.ds-py-3"))
#             )
            
#             html = self.driver.page_source
#             self.parser.set_html(html)
#             matches = self.parser.parse()
            
#             current_time = datetime.now().isoformat()
#             for match in matches:
#                 self.next(
#                     series=match.series,
#                     team1=match.team1,
#                     team2=match.team2,
#                     score1=match.score1,
#                     score2=match.score2,
#                     over1=match.over1,
#                     over2=match.over2,
#                     status=match.status,
#                     timestamp=current_time,
#                     source="ESPN Cricinfo"
#                 )
                
#         except Exception as e:
#             print(f"Scraping error: {str(e)}")
#             raise  # Re-raise for retry handling

# class CricketMatchSchema(pw.Schema):
#     series: str
#     team1: str
#     team2: str
#     score1: str
#     score2: str
#     over1: str
#     over2: str
#     status: str
#     timestamp: str
#     source: str

# def create_cricket_stream(refresh_interval: int = Config.REFRESH_INTERVAL) -> pw.Table:
#     subject = CricketMatchSubject(refresh_interval)
#     return pw.io.python.read(
#         subject,
#         schema=CricketMatchSchema
#     )




# import requests
# from bs4 import BeautifulSoup
# import json
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# class Scraper:
#     def __init__(self, player_name):
#         self.driver = None
#         self.player_name = player_name
#         self.base_url = "https://www.howstat.com"

#     def get_player_id(self):
#         url = self.driver.current_url
#         if "PlayerID=" in url:
#             return url.split("PlayerID=")[1]
#         return None

#     def get_player_info(self, soup):
#         data = {}
#         for row in soup.find_all("td", class_="FieldName2"):
#             key = row.get_text(strip=True).replace("\xa0", " ")
#             value_td = row.find_next_sibling("td")
#             value = value_td.get_text(strip=True) if value_td else ""
#             data[key.rstrip(":")] = value
#             print(f"{key}:{value}")

#         return data

#         # for k, v in data.items():
#         #    print(f"{k}:{v}")

#     def source_table_data(self, soup):
#         tables = soup.find_all("table", class_="BorderedBox3")
#         all_stats = []
#         for table in tables:
#             stats = self.extract_table_data(table)
#             all_stats.append(stats)
        
#         formats = ["Tests", "ODIs", "T20s", "Overall", "IPL"]
#         for index, stats in enumerate(all_stats):
#             if index < len(formats):
#                 stats["Format"] = formats[index]
        
#         return all_stats  # Return data instead of saving to JSON

#     def start(self):
#         options = Options()
#         options.add_argument("--headless")
#         self.driver = webdriver.Chrome(options=options)
        
#         try:
#             self.driver.get("https://www.howstat.com/Cricket/Statistics/Players/PlayerMenu.asp")
#             search_input = self.driver.find_element(By.ID, "txtPlayer")
#             search_input.send_keys(self.player_name)
#             search_input.send_keys(Keys.RETURN)
#             time.sleep(2)

#             player_search_name = self.driver.find_elements(By.CLASS_NAME, "LinkTable")
#             if not player_search_name:
#                 return {"error": f"Player '{self.player_name}' not found"}
#             player_search_name[0].click()

#             WebDriverWait(self.driver, 10).until(
#                 EC.presence_of_element_located((By.TAG_NAME, "body"))
#             )
#             soup = BeautifulSoup(self.driver.page_source, "html.parser")

#             player_info = self.get_player_info(soup)
#             stats = self.source_table_data(soup)
            
#             return {
#                 "player_info": player_info,
#                 "stats": stats
#             }
#         except Exception as e:
#             return {"error": str(e)}
#         finally:
#             self.driver.quit()




# import requests
# from bs4 import BeautifulSoup
# import json
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager

# class Scraper:
#     def __init__(self, player_name):
#         self.player_name = player_name
#         self.options = Options()
#         self.options.add_argument("--headless=new")  # New headless mode
#         self.options.add_argument("--no-sandbox")    # Required for WSL/Linux
#         self.options.add_argument("--disable-dev-shm-usage")  # Prevents crashes
#         self.service = Service(ChromeDriverManager().install())
#         self.driver = None
#         self.player_name = player_name
#         self.base_url = "https://www.howstat.com"

#     def get_player_id(self):
#         url = self.driver.current_url
#         if "PlayerID=" in url:
#             return url.split("PlayerID=")[1]
#         return None

#     def get_player_info(self, soup):
#         data = {}
#         for row in soup.find_all("td", class_="FieldName2"):
#             key = row.get_text(strip=True).replace("\xa0", " ")
#             value_td = row.find_next_sibling("td")
#             value = value_td.get_text(strip=True) if value_td else ""
#             data[key.rstrip(":")] = value
#             print(f"{key}:{value}")

#         return data

#         # for k, v in data.items():
#         #    print(f"{k}:{v}")

#     def source_table_data(self, soup):
#         tables = soup.find_all("table", class_="BorderedBox3")
#         all_stats = []
#         for table in tables:
#             stats = self.extract_table_data(table)
#             all_stats.append(stats)
#         formats = ["Tests", "ODIs", "T20s", "Overall", "IPL"]
#         for index, stats in enumerate(all_stats):
#             if index < 6:
#                 stats["Format"] = formats[index]

#         print(all_stats)  # uncomment to debug

#         json_output = json.dumps(all_stats, indent=4)
#         with open("player_stats.json", "w") as f:
#             f.write(json_output)
#         return json_output

#     def extract_table_data(self, table):
#         stats = {}
#         rows = table.find_all("tr")
#         current_section = None

#         for row in rows:
#             cols = row.find_all("td")
#             if len(cols) == 2:
#                 key_span = cols[0].find("span", class_="FieldName2")
#                 value_td = cols[1].text.strip()
#                 if key_span:
#                     key = key_span.text.strip().replace(":", "")
#                     stats[key] = value_td
#             elif len(cols) == 1 and "background-color" in str(cols[0].get("style", "")):
#                 # Category header
#                 current_section = cols[0].text.strip()
#                 stats[current_section] = {}
#             elif len(cols) == 2 and current_section:
#                 key_span = cols[0].find("span", class_="FieldName2")
#                 value_td = cols[1].text.strip()
#                 if key_span:
#                     key = key_span.text.strip().replace(":", "")
#                     stats[current_section][key] = value_td

#         return stats

#     def start(self):
#         options = Options()
#         options.add_argument("--headless")
#         self.driver = webdriver.Chrome(service=self.service, options=self.options)

#         try:
#             self.driver.get(
#                 "https://www.howstat.com/Cricket/Statistics/Players/PlayerMenu.asp")
#             search_input = self.driver.find_element(By.ID, "txtPlayer")
#             search_input.send_keys(self.player_name)
#             search_input.send_keys(Keys.RETURN)
#             time.sleep(2)

#             player_search_name = self.driver.find_elements(
#                 By.CLASS_NAME, "LinkTable")
#             player_search_name[0].click()

#             WebDriverWait(self.driver, 10).until(
#                 EC.presence_of_element_located((By.TAG_NAME, "body"))
#             )
#             soup = BeautifulSoup(self.driver.page_source, "html.parser")

#             # self.get_player_id()
#             self.get_player_info(soup)
#             self.source_table_data(soup)

#         finally:
#             self.driver.quit()



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
from webdriver_manager.chrome import ChromeDriverManager

class Scraper:
    def __init__(self, player_name):
        # Initialize Chrome options
        self.options = Options()
        self.options.add_argument("--headless=new")  # New headless mode
        self.options.add_argument("--no-sandbox")    # Required for WSL/Linux
        self.options.add_argument("--disable-dev-shm-usage")  # Prevents crashes
        self.options.add_argument("--disable-gpu")  # Additional stability
        
        # Initialize service with ChromeDriverManager
        self.service = Service(ChromeDriverManager().install())
        
        # Initialize other attributes
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
            print(f"{key}:{value}")
        return data

    def source_table_data(self, soup):
        tables = soup.find_all("table", class_="BorderedBox3")
        all_stats = []
        for table in tables:
            stats = self.extract_table_data(table)
            all_stats.append(stats)
        
        formats = ["Tests", "ODIs", "T20s", "Overall", "IPL"]
        for index, stats in enumerate(all_stats):
            if index < len(formats):
                stats["Format"] = formats[index]

        json_output = json.dumps(all_stats, indent=4)
        with open("player_stats.json", "w") as f:
            f.write(json_output)
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
        try:
            # Initialize driver with configured options
            self.driver = webdriver.Chrome(service=self.service, options=self.options)
            
            # Main scraping logic
            self.driver.get("https://www.howstat.com/Cricket/Statistics/Players/PlayerMenu.asp")
            
            # Search for player
            search_input = self.driver.find_element(By.ID, "txtPlayer")
            search_input.send_keys(self.player_name)
            search_input.send_keys(Keys.RETURN)
            time.sleep(2)  # Wait for search results

            # Click on first result
            player_search_name = self.driver.find_elements(By.CLASS_NAME, "LinkTable")
            if not player_search_name:
                raise Exception("Player not found")
            player_search_name[0].click()

            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Parse and process data
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            self.get_player_info(soup)
            return self.source_table_data(soup)
            
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
            raise
        finally:
            if self.driver:
                self.driver.quit()
from selenium import webdriver

class BaseScraper:
    def __init__(self, driver: webdriver):
        self.driver = driver

    def navigate_to(self, url: str):
        self.driver.get(url)

    def get_page_source(self) -> str:
        return self.driver.page_source

    def close(self):
        self.driver.close()
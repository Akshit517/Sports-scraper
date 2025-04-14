from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class BaseDriver:
    def __init__(self, binary_path=None):
        options = Options()
        options.add_argument("--headless")
        # options.headless = True
        if binary_path:
            options.binary_location = binary_path
        self.driver = webdriver.Firefox(options=options)

    def get_driver(self):
        return self.driver

    def get_page_source(self):
        return self.driver.page_source

    def quit(self):
        self.driver.quit()

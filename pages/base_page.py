class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open_url(self, url: str):
        self.driver.get(url)

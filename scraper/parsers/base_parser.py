from bs4 import BeautifulSoup

class BaseParser:
    def __init__(self, html_content: str):
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def parse(self):
        raise NotImplementedError("Subclasses must implement parse()")
    
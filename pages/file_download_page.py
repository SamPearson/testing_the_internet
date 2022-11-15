
from selenium.webdriver.common.by import By
from . base_page import BasePage
import time
import http.client


class DownloadPage(BasePage):
    _download_links = {"by": By.CSS_SELECTOR, "value": ".example a"}

    def __init__(self, driver):
        self.driver = driver
        self._visit("/download")

    def get_link(self, link_text):
        return self.get_links(link_text)[0]

    def get_links(self, link_text):
        links = self._find_all(self._download_links)
        matches = [link.get_attribute('href') for link in links
                   if link_text in link.text]

        if matches:
            return matches
        else:
            return False

    def request_headers(self, url):
        connection = http.client.HTTPConnection(self.driver.base_domain)
        connection.request('HEAD', url)
        response = connection.getresponse()

        return response

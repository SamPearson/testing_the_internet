
from selenium.webdriver.common.by import By
from . base_page import BasePage
import time
import http.client


class DownloadPage(BasePage):
    _first_download_link = {"by": By.CSS_SELECTOR, "value": ".example a"}

    def __init__(self, driver):
        self.driver = driver
        self._visit("/download")

    def get_link(self):
        pass
        #  Get list of A elements
        #  parse list of A element, collect exact matches

    def download_first_file(self):
        self._find(self._first_download_link).click()
        time.sleep(1.0)  # ETA for files downloaded with selenium must be Estimated

    def fetch_first_file_headers(self):
        link = self._find(self._first_download_link).get_attribute('href')
        connection = http.client.HTTPConnection(self.driver.base_domain)
        connection.request('HEAD', link)
        response = connection.getresponse()

        return response

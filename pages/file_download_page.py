
from selenium.webdriver.common.by import By
from . base_page import BasePage
import tempfile
import time
import os
from selenium import webdriver


class DownloadPage(BasePage):
    _first_download_link = {"by": By.CSS_SELECTOR, "value": ".example a"}

    def __init__(self, driver):
        self.driver = driver
        self._visit("/download")

    def download_first_file(self):
        self._find(self._first_download_link).click()
        time.sleep(1.0)  # ETA for files downloaded with selenium must be Estimated


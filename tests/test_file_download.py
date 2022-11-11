import pytest
from pages import file_download_page
import shutil
import os


@pytest.mark.download
class TestFileDownload:
    @pytest.fixture
    def download_page(self, driver, request):
        return file_download_page.DownloadPage(driver)

    @pytest.mark.smoke
    def test_download_file(self, download_page):
        # Selenium can be used to inspect or interact with elements on the page
        # It is not meant to be used to test a browser's file download ability.
        pass  # download_page.download_first_file()

        #  assert about a downloaded file

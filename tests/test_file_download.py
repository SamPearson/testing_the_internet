import pytest
from pages import file_download_page


@pytest.mark.download
class TestFileDownload:
    @pytest.fixture
    def download_page(self, driver, request):
        return file_download_page.DownloadPage(driver)

    @pytest.mark.smoke
    def test_download_file_headers(self, download_page):

        headers = download_page.fetch_first_file_headers()
        content_type = headers.getheader('Content-type')
        content_length = int(headers.getheader('Content-length'))

        assert content_type == 'application/octet-stream'
        assert content_length > 0

import pytest
from pages import file_upload_page
import os


@pytest.mark.upload
class TestFileUpload:
    @pytest.fixture
    def upload(self, driver):
        return file_upload_page.UploadPage(driver)

    @pytest.mark.smoke
    def test_upload_file(self, upload):
        #create file
        filename = "upload_test_file.txt"
        path = os.path.join(os.getcwd(), "assets", filename)
        upload.file_(path)

        assert upload.uploaded_filename() == filename


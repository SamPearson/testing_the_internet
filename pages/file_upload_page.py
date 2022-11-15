
from selenium.webdriver.common.by import By
from . base_page import BasePage


class UploadPage(BasePage):
    _file_browse_button = {"by": By.ID, "value": "file-upload"}
    _submit_button = {"by": By.ID, "value": "file-submit"}
    _dragon_drop_field = {"by": By.ID, "value": "drag-drop-upload"}
    _uploaded_files = {"by": By.ID, "value": "uploaded-files"}

    def __init__(self, driver):
        self.driver = driver
        self._visit("/upload")
        for element in [
            self._file_browse_button,
            self._submit_button,
            self._dragon_drop_field
                        ]:
            assert self._is_displayed(element)

    def file_(self, path):
        self._type(self._file_browse_button, path)
        self._click(self._submit_button)

    def file_uploaded(self):
        return self._is_displayed(self._uploaded_files)

    def uploaded_filename(self):
        return self._find(self._uploaded_files).text

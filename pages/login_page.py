from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    _login_form = (By.ID, "login")
    _username_input = (By.ID, "username")
    _password_input = (By.ID, "password")
    _submit_button = (By.CSS_SELECTOR, "button")

    _success_message = (By.CSS_SELECTOR, ".flash.success")
    _failure_message = (By.CSS_SELECTOR, ".flash.error")

    def __init__(self, driver):
        self.driver = driver
        self._visit("/login")
        import time
        time.sleep(10)
        assert self._is_displayed(self._login_form)

    def with_(self, username, password):
        self._type(self._username_input, username)
        self._type(self._password_input, password)
        self._click(self._submit_button)

    def success_message_present(self):
        return self._is_displayed(self._success_message, 1)

    def failure_message_present(self):
        return self._is_displayed(self._failure_message, 1)

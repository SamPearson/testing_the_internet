import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from pages import login_page


class TestLogin:
    @pytest.fixture
    def login(self, request):
        driver_ = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        driver_.implicitly_wait(5)

        def quit():
            driver_.quit()

        request.addfinalizer(quit)
        return login_page.LoginPage(driver_)

    def test_valid_credentials(self, login):
        login.with_("tomsmith", "SuperSecretPassword!")
        assert login.success_message_present()

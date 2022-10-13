import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


class TestFirst:
    @pytest.fixture
    def driver(self, request):
        driver_ = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        driver_.implicitly_wait(5)

        def quit():
            driver_.quit()

        request.addfinalizer(quit)
        return driver_

    def test_valid_credentials(self, driver):
        driver.get("https://the-internet.herokuapp.com/login")
        driver.find_element(By.ID, "username").send_keys("tomsmith")
        driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        driver.find_element(By.CSS_SELECTOR, "button").click()
        assert driver.find_element(By.CSS_SELECTOR, ".flash.success").is_displayed()




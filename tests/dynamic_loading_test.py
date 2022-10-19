
import pytest
import os
from selenium import webdriver
from pages import dynamic_loading_page
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


class TestDynamicLoading():

    @pytest.fixture
    def dynamic_loading(self, request):
        driver_ = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

        def quit():
            driver_.quit()

        request.addfinalizer(quit)
        return dynamic_loading_page.DynamicLoadingPage(driver_)

    def test_hidden_element(self, dynamic_loading):
        dynamic_loading.load_example("1")
        assert dynamic_loading.finish_text_present()

    def test_rendered_element(self, dynamic_loading):
        dynamic_loading.load_example("2")
        assert dynamic_loading.finish_text_present()
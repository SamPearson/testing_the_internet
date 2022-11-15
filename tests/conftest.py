
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from . import config
import os
import re


def pytest_addoption(parser):
    parser.addoption("--baseurl",
                     action="store",
                     default="https://the-internet.herokuapp.com",
                     help="base URL for the application under test")
    parser.addoption("--host",
                     action="store",
                     default="saucelabs",
                     help="where to run your tests: localhost or saucelabs")
    parser.addoption("--browser",
                     action="store",
                     default="firefox",
                     help="the name of the browser you want to test with")
    parser.addoption("--browserversion",
                     action="store",
                     default="latest",
                     help="the browser version you want to test with")
    parser.addoption("--platform",
                     action="store",
                     default="Windows 7",
                     help="the operating system to run your tests on (saucelabs only)")


@pytest.fixture
def driver(request):
    config.baseurl = request.config.getoption("--baseurl")
    config.host = request.config.getoption("--host").lower()
    config.browser = request.config.getoption("--browser").lower()
    config.browserversion = request.config.getoption("--browserversion").lower()
    config.platform = request.config.getoption("--platform").lower()

    if config.host == "saucelabs":
        # If using jenkins, saucelabs credentials must be set manually, as described below
        # https://docs.saucelabs.com/ci/jenkins/
        _credentials = os.getenv("SAUCE_USERNAME") + ":" + os.getenv(
            "SAUCE_ACCESS_KEY")
        _url = "https://" + _credentials + "@ondemand.us-west-1.saucelabs.com:443/wd/hub"

        _desired_caps = {"browserName": config.browser, "browserVersion": config.browserversion,
                         "platformName": config.platform,
                         "name": request.cls.__name__ + "." + request.function.__name__}

        driver_ = webdriver.Remote(_url, _desired_caps)

    elif config.host == "localhost":
        driver_ = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))


    driver_.base_url = config.baseurl
    driver_.base_domain = re.sub(".*//","",config.baseurl)

    def quit_browser():
        try:
            if config.host == "saucelabs":
                if request.node.result_call.failed:
                    driver_.execute_script("sauce:job-result=failed")
                    print("https://saucelabs.com/tests/" + driver_.session_id)
                elif request.node.result_call.passed:
                    driver_.execute_script("sauce:job-result=passed")
        finally:
            driver_.quit()

    request.addfinalizer(quit_browser)
    return driver_


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    setattr(item, "result_" + result.when, result)

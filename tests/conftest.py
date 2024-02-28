
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from env_config import test_env_config
import os


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
    test_env_config.baseurl = request.config.getoption("--baseurl")
    test_env_config.host = request.config.getoption("--host").lower()
    test_env_config.browser = request.config.getoption("--browser").lower()
    test_env_config.browserversion = request.config.getoption("--browserversion").lower()
    test_env_config.platform = request.config.getoption("--platform").lower()

    if test_env_config.host == "saucelabs":
        # If using jenkins, saucelabs credentials must be set manually, as described below
        # https://docs.saucelabs.com/ci/jenkins/
        _credentials = os.getenv("SAUCE_USERNAME") + ":" + os.getenv(
            "SAUCE_ACCESS_KEY")
        _url = "https://" + _credentials + "@ondemand.us-west-1.saucelabs.com:443/wd/hub"

        _desired_caps = {"browserName": test_env_config.browser, "browserVersion": test_env_config.browserversion,
                         "platformName": test_env_config.platform,
                         "name": request.cls.__name__ + "." + request.function.__name__}

        driver_ = webdriver.Remote(_url, _desired_caps)

    elif test_env_config.host == "localhost":
        driver_ = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))


    driver_.base_url = test_env_config.baseurl
    driver_.base_domain = re.sub(".*//","",test_env_config.baseurl)

    def quit_browser():
        try:
            if test_env_config.host == "saucelabs":
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

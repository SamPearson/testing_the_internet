import pytest
from pages import login_page


@pytest.mark.login
class TestLogin:
    @pytest.fixture
    def login(self, driver):
        return login_page.LoginPage(driver)

    @pytest.mark.smoke
    def test_valid_credentials(self, login):
        login.with_("tomsmith", "SuperSecretPassword!")
        assert login.success_message_present()

    @pytest.mark.midweight
    def test_invalid_credentials(self, login):
        login.with_("tomsmith", "bad password")
        assert login.failure_message_present()


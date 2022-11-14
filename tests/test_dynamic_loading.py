
import pytest
from pages import dynamic_loading_page


@pytest.mark.dynamicLoading
class TestDynamicLoading():

    @pytest.fixture
    def dynamic_loading(self, driver):
        return dynamic_loading_page.DynamicLoadingPage(driver)

    @pytest.mark.smoke
    def test_hidden_element(self, dynamic_loading):
        dynamic_loading.load_example("1")
        assert dynamic_loading.finish_text_present()

    @pytest.mark.smoke
    def test_rendered_element(self, dynamic_loading):
        dynamic_loading.load_example("2")
        assert dynamic_loading.finish_text_present()
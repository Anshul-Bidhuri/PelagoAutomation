import pytest
from Pages.homepage import Homepage
from Helpers import assertion_methods
from Data import constant


@pytest.mark.FamousDestinationSection
class TestFamousDestinationSection:

    @pytest.fixture(scope="class", autouse=True)
    def initiate_driver(self, request, initiate_browser_webdriver):
        request.cls.driver = initiate_browser_webdriver
        request.cls.driver.get(constant.HOME_PAGE_URL.get(request.cls.server))
        request.cls.home_page_obj = Homepage(request.cls.driver)

    def test_famous_destination_links_status_code(self):
        """
        Checks that all famous destination tile links on the homepage are reachable (status code 200).
        """
        links = self.home_page_obj.get_famous_destination_tile_links()
        assertion_methods.check_status_code_of_urls(urls=links)

    def test_famous_destination_images_status_code(self, initiate_browser_webdriver):
        """
        Checks that all famous destination images on the homepage load successfully (status code 200).
        """
        images = self.home_page_obj.get_famous_destination_images()
        assertion_methods.check_status_code_of_urls(urls=images)

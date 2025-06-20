import pytest_check as check
import pytest
import locators
from Utility import api_services
from Helpers import driver_helpers
from Pages.homepage import Homepage


class TestFamousDestinationSection:

    @pytest.fixture(scope="class", autouse=True)
    def initiate_driver(self, request, initiate_browser_webdriver):
        request.cls.home_page_obj = Homepage(self.driver)

    def test_famous_destination_links_status_code(self):
        self.home_page_obj.get_famous_detination_tile_links()

    def test_famous_destination_images_status_code(self, initiate_browser_webdriver):
        driver = initiate_browser_webdriver
        driver_helpers.wait_till_element_is_present(driver, locators.famous_destinations_title_xpath)
        famous_destinations = driver_helpers.get_all_elements(driver, locators.famous_destinations_title_xpath)
        print(f"famous destinations found: {len(famous_destinations)}")
        for destination in famous_destinations:
            driver_helpers.click_element(driver, element=destination, timeout=10)
            img_elements = driver_helpers.get_all_elements(driver, locators.famous_destinations_image_under_each_title_xpath)
            print(f"Images found: {len(img_elements)}")
            for img_element in img_elements:
                image_url = driver_helpers.get_element_attribute_value(driver=driver, element=img_element, attribute_name="href")
                status_code = api_services.return_status_code_of_url(api_url=image_url, method_name="get")
                check.equal(status_code, 200, msg=f"{image_url} status code is {status_code} not 200")

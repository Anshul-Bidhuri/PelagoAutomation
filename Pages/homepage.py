import sys, os

main_project_path = os.path.abspath(__file__+"../../../")
print(main_project_path)
sys.path.append(main_project_path)

from Pages.basepage import BasePage
from Helpers import driver_helpers
import locators
from Utility import api_services


class Homepage(BasePage):

    def get_famous_destination_tile_links(self):
        driver_helpers.wait_till_element_is_present(self.driver, locators.famous_destinations_title_xpath)
        famous_destinations = driver_helpers.get_all_elements(self.driver, locators.famous_destinations_title_xpath)
        print(f"famous destinations found: {len(famous_destinations)}")
        for destination in famous_destinations:
            driver_helpers.click_element(self.driver, element=destination, timeout=10)
            links = driver_helpers.get_all_elements(self.driver, locators.famous_destinations_link_under_each_title_xpath)
            print(f"links found: {len(links)}")
            for link_element in links:
                link = driver_helpers.get_element_attribute_value(driver=self.driver, element=link_element,
                                                                  attribute_name="href")
                status_code = api_services.return_status_code_of_url(api_url=link, method_name="get")
                # check.equal(status_code, 200, msg=f"{link} status code is {status_code} not 200")
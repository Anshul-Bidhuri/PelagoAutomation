import sys, os
import time

main_project_path = os.path.abspath(__file__+"../../../")
sys.path.append(main_project_path)

from Pages.basepage import BasePage
from Helpers import driver_helpers, custom_logger
import locators

log = custom_logger.get_logger()

class Homepage(BasePage):

    def get_famous_destinations_elements(self):
        driver_helpers.wait_till_element_is_present(self.driver, locators.famous_destinations_title_xpath)
        famous_destinations = driver_helpers.get_all_elements(self.driver, locators.famous_destinations_title_xpath)
        log.info(f"famous destinations found: {len(famous_destinations)}")
        return famous_destinations

    def get_famous_destination_tile_links(self):
        total_links = []
        famous_destinations = self.get_famous_destinations_elements()
        for destination in famous_destinations:
            driver_helpers.click_element(self.driver, element=destination, timeout=10)
            links = driver_helpers.get_all_elements(self.driver, locators.famous_destinations_link_under_each_title_xpath)
            log.info(f"links found: {len(links)}")
            for link_element in links:
                link = driver_helpers.get_element_attribute_value(driver=self.driver, element=link_element, attribute_name="href")
                total_links.append(link)
        log.info(f"total links: {total_links}")
        return total_links

    def get_famous_destination_images(self):
        images_links = []
        famous_destinations = self.get_famous_destinations_elements()
        for destination in famous_destinations:
            driver_helpers.click_element(self.driver, element=destination, timeout=10)
            img_elements = driver_helpers.get_all_elements(self.driver, locators.famous_destinations_image_under_each_title_xpath)
            log.info(f"Images found: {len(img_elements)}")
            for img_element in img_elements:
                image_url = driver_helpers.get_element_attribute_value(driver=self.driver, element=img_element, attribute_name="src")
                images_links.append(image_url)
        log.info(f"images links: {images_links}")
        return images_links

from selenium import webdriver
import driver_helpers, locators, api_services

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.pelago.com/en/")
driver_helpers.wait_till_element_is_present(driver, locators.famous_destinations_title_xpath)
famous_destinations = driver_helpers.get_all_elements(driver, locators.famous_destinations_title_xpath)
print(f"famous destinations found: {len(famous_destinations)}")
for destination in famous_destinations:
    driver_helpers.click_element(driver, element=destination, timeout=10)
    links = driver_helpers.get_all_elements(driver, locators.famous_destinations_link_under_each_title_xpath)
    print(f"links found: {len(links)}")
    for link_element in links:
        link = link_element.get_attribute("href")
        status_code = api_services.return_status_code_of_url(api_url=link, method_name="get")
        assert status_code==200
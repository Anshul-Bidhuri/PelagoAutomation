from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException, ElementClickInterceptedException, WebDriverException, ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
from typing import Union

import locators


def get_locator_type(locator):
    for name, val in vars(locators).items():
        if val is locator:
            locator_mapping = {"css": By.CSS_SELECTOR, "xpath": By.XPATH, "id": By.ID}
            locator_type = locator_mapping[name.split("_")[-1]]
            return locator_type


def get_element_attribute_value(driver, locator=None, element=None, attribute_name=None):
    # attribute_value = element.get_attribute(attribute_name) if element else wait_till_element_is_present(driver, locator).get_attribute(attribute_name)
    if element:
        attribute_value = element.get_attribute(attribute_name)
    elif locator:
        attribute_value = wait_till_element_is_present(driver, locator).get_attribute(attribute_name)
    else:
        print("ERROR: element or locator not found")
        attribute_value = None
    return attribute_value


def wait_till_element_is_present(driver: WebDriver, locator: str, timeout: int = 30) -> Union[WebElement, bool]:
    """
    Waits until the element is present in the DOM (not necessarily visible) within the specified timeout.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        locator (str): The locator string (e.g., XPath, CSS Selector, etc.).
        timeout (int, optional): Maximum time to wait for the element in seconds. Default is 30.

    Returns:
        WebElement: The found element if present within the timeout.
        bool: False if the element is not found within the timeout.

    Raises:
        None: Handles TimeoutException internally and returns False instead.
    """
    try:
        element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((get_locator_type(locator), locator)))
        print(f"{locator} is present")
        return element
    except TimeoutException as e:
        print(f"ERROR: timeout error, locator '{locator}' not found")
        return False

def get_all_elements(driver, locator):
    all_elements = driver.find_elements(get_locator_type(locator), locator)
    return all_elements


def wait_till_element_is_clickable(driver, locator=None, element=None, timeout=30):
    if locator:
        element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((get_locator_type(locator), locator)))
        print(f"{locator} is clickable")
    elif element:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(element))
        print("element clickable")
    return element


def click_element(driver, locator=None, element=None, timeout=30): # try to click, if fail check popup, if popup present, close popup then retry
    try:
        element.click() if element else wait_till_element_is_clickable(driver, locator=locator, timeout=timeout).click()
    except (ElementClickInterceptedException, ElementNotInteractableException):
        print("ElementClickInterceptedException occurred, checking for popup...")
        popup = wait_till_element_is_clickable(driver, locator=locators.campaign_pop_up_xpath, timeout=5)
        if popup:
            popup.click()
            print("Popup closed. Retrying element click.")
            try:
                wait_till_element_is_clickable(driver, locator, element, timeout)
                ActionChains(driver).move_to_element(element).click().perform()
            except Exception as retry_exception:
                print(f"Retry failed: {retry_exception}")
        else:
            print("Popup not found or not clickable.")
    except WebDriverException as e:
        print(f"WebDriverException occurred during click: {e}")
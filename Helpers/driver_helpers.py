from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException, ElementClickInterceptedException, WebDriverException, ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
from typing import Union
from selenium import webdriver


import locators


def get_locator_type(locator: str) -> str:
    """
    Determines the Selenium locator type based on the locator string.

    Args:
        locator (str): The locator string to analyze.

    Returns:
        str: The Selenium By strategy (e.g., By.CSS_SELECTOR, By.XPATH, By.ID).
    """
    for name, val in vars(locators).items():
        if val is locator:
            locator_mapping = {"css": By.CSS_SELECTOR, "xpath": By.XPATH, "id": By.ID}
            locator_type = locator_mapping[name.split("_")[-1]]
            return locator_type


def get_element_attribute_value(driver: WebDriver, locator: str = None, element: WebElement = None, attribute_name: str = None, timeout: int = 10) -> str:
    """
    Retrieves the value of the specified attribute from a web element, waiting until it is not None or empty.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        locator (str, optional): The locator string to find the element. Either locator or element must be provided.
        element (WebElement, optional): The web element to get the attribute from.
        attribute_name (str, optional): The name of the attribute to retrieve.
        timeout (int, optional): Maximum time to wait for the attribute to be non-empty. Defaults to 10 seconds.

    Returns:
        str: The value of the attribute, or None if the element or attribute is not found within the timeout.
    """
    attribute_value = None
    try:
        if element:
            WebDriverWait(driver, timeout).until(lambda d: element.get_attribute(attribute_name))
            attribute_value = element.get_attribute(attribute_name)
        elif locator:
            web_elem = wait_till_element_is_present(driver, locator)
            WebDriverWait(driver, timeout).until(lambda d: web_elem.get_attribute(attribute_name))
            attribute_value = web_elem.get_attribute(attribute_name)
        else:
            print("ERROR: element or locator not found")
    except TimeoutException:
        print(f"Timeout: Attribute '{attribute_name}' did not become available/non-empty within {timeout} seconds.")
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

def get_all_elements(driver: WebDriver, locator: str) -> list[WebElement]:
    """
    Finds all elements matching the given locator.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        locator (str): The locator string to find elements.

    Returns:
        list[WebElement]: A list of WebElements matching the locator, or an empty list if none are found.
    """
    wait_till_element_is_present(driver, locator, timeout=3)
    all_elements = driver.find_elements(get_locator_type(locator), locator)
    return all_elements


def wait_till_element_is_clickable(driver: WebDriver, locator: str = None, element: WebElement = None, timeout: int = 30) -> WebElement:
    """
    Waits until the element is clickable within the specified timeout.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        locator (str, optional): The locator string to find the element. Either locator or element must be provided.
        element (WebElement, optional): The web element to wait for.
        timeout (int, optional): Maximum time to wait in seconds. Default is 30.

    Returns:
        WebElement: The clickable WebElement.

    Raises:
        TimeoutException: If the element is not clickable within the timeout.
    """
    if locator:
        element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((get_locator_type(locator), locator)))
        print(f"{locator} is clickable")
    elif element:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(element))
        print("element clickable")
    return element


def click_element(driver: WebDriver, locator: str = None, element: WebElement = None, timeout: int = 30) -> None:
    """
    Clicks on the specified element, handling potential popup interceptions.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        locator (str, optional): The locator string to find the element. Either locator or element must be provided.
        element (WebElement, optional): The web element to click.
        timeout (int, optional): Maximum time to wait in seconds. Default is 30.

    Returns:
        None

    Note:
        If the initial click fails due to an intercepted exception, it will attempt to close any popup and retry the click.
    """
    try:
        element.click() if element else wait_till_element_is_clickable(driver, locator=locator, timeout=timeout).click()
        print("Element clicked successfully")
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


def initialize_chrome_driver(headless=False) -> WebDriver:
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--ignore-certificate-errors")
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver


def initialize_safari_driver(headless=False) -> WebDriver:
    options = webdriver.SafariOptions()
    driver = webdriver.Safari(options=options)
    driver.maximize_window()
    if headless:
        options.add_argument("--headless")
    return driver


def initialize_firefox_driver(headless=False) -> WebDriver:
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument('--headless')
    options.set_preference('dom.webnotifications.enabled', False)  # Disable notifications
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()  # Maximize the browser window
    return driver
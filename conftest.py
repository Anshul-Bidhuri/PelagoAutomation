import pytest

from selenium import webdriver


@pytest.fixture(scope="class")
def initiate_browser_webdriver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    # driver.get("https://www.pelago.com/en/")
import pytest

from Helpers import driver_helpers


@pytest.fixture(scope="class")
def initiate_browser_webdriver(request):
    browser_option = request.config.getoption("Browser")
    server_option = request.config.getoption("Server")
    headless_option = request.config.getoption("Headless")
    request.cls.server = server_option
    driver_options = {
        "chrome": driver_helpers.initialize_chrome_driver,
        "firefox": driver_helpers.initialize_firefox_driver,
        "safari": driver_helpers.initialize_safari_driver}
    driver = driver_options[browser_option](headless_option)
    yield driver
    driver.quit()


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group._addoption(
        "-B",
        dest="Browser",
        default="chrome",
        help="Browser to use. Options are: chrome, firefox and safari. Example: -B firefox",
    )
    group._addoption(
        "-S",
        dest="Server",
        default="PROD",
        help="Server to use. Options are: QA, PROD. Example: -S PROD",
    )
    group._addoption(
        "-H",
        dest="Headless",
        default=False,
        help="Run in headless mode. Example: -H True",
    )
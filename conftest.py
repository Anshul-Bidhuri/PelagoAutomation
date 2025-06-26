import pytest
from py.xml import html

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


def pytest_html_results_summary(prefix):
    prefix.extend([html.p("This UI Automation regression framework is created by ANSHUL BIDHURI")])


def pytest_html_results_table_header(cells):
    cells.insert(1, html.th("Description"))
    cells.pop(2)
    cells.pop()  # to remove last column name


def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))
    cells.pop(2)
    cells.pop()  # to remove last row values


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)

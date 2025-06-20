from Utility import api_services
from pytest_check import check


def check_status_code_of_urls(urls: list):
    for url in urls:
        status_code = api_services.return_status_code_of_url(api_url=url, method_name="get")
        check.equal(status_code, 200, msg=f"{url} status code is {status_code} not 200")
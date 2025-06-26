import requests
from Helpers import custom_logger

log = custom_logger.get_logger()


def return_status_code_of_url(api_url, method_name):
    response = requests.request(method=method_name, url=api_url)
    status_code = response.status_code
    log.info(f"status code of {api_url} is: {status_code}")
    return status_code


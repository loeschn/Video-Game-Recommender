import pymongo
import requests

class ScrapingException(Exception):
    pass

def api_request(url, params=None):
    """Make an IGDB API request."""
    headers = {'Accept': 'application/json',
               "user-key": '1cca0ffb6c7bbc063e1ae12727218933'}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise ScrapingException(f"Error: status code {response.status_code}\n\nContent:\n{response.content}")
    return response.json()



def api_endpoint(endpoint="", endpoint_id=""):
    """Make a request for an endpoint & endpoint_id.
        A generalized api request funtion"""

    url = f"https://api-2445582011268.apicast.io/{endpoint}/{endpoint_id}"
    return api_request(url)

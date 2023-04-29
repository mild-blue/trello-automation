import requests

from my_secrets import TRELLO_KEY, TRELLO_TOKEN


def make_trello_request(url_add_on: str, method: str = 'GET', params: dict = None, data: dict = None):
    headers = {
        'Accept': 'application/json'
    }
    full_url = f'https://api.trello.com/1/{url_add_on}'
    full_data = {'key': TRELLO_KEY, 'token': TRELLO_TOKEN}
    if data:
        full_data.update(data)
    response = requests.request(
        method=method,
        url=full_url,
        headers=headers,
        params=params,
        data=full_data
    )
    if response.status_code == 200:
        return response
    else:
        response.raise_for_status()

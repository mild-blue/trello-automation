import requests
import json
import datetime
from my_secrets import *
from my_settings import *


def make_request(url: str, method: str = "GET", params: dict = None, data: dict = None):
    headers = {
        "Accept": "application/json"
    }
    full_params = {'key': trelloKey, 'token': trelloToken}
    if params:
        full_params.update(params)

    response = requests.request(
        method,
        url,
        headers=headers,
        params=full_params,
        data=data
    )
    return response


def search_board(searched_board_id):
    response = make_request(mainEndpoint + "boards/" + searched_board_id + "/lists")
    lists_on_board = json.loads(response.text)
    for list in lists_on_board:
        if list['id'] != target_list_id:
            search_list(list['id'])


def search_list(searched_list_id):
    response = make_request(mainEndpoint + "lists/" + searched_list_id + "/cards")
    cards_on_list = json.loads(response.text)
    for card in cards_on_list:
        for user_id in members_id:
            if (user_id in card['idMembers']) and (check_date(card['id'])):
                copy_card(card['id'], target_list_id)


def copy_card(card_id, target_list_id):
    make_request(url=mainEndpoint + "cards",
                 method="POST",
                 params={"idList": target_list_id, "idCardSource": card_id}
                 )


def check_date(card_id):
    response = make_request(mainEndpoint + "cards/" + card_id + "/due")
    date_on_card = json.loads(response.text)
    unformatted_date = date_on_card['_value'].split('T')
    card_year, card_month, card_day = map(int, unformatted_date[0].split('-'))
    card_date = datetime.date(card_year, card_month, card_day)
    return card_date <= furthest_date


if __name__ == '__main__':
    mainEndpoint = "https://api.trello.com/1/"
    day, month, year = map(int, input_furthest_date.split('.'))
    furthest_date = datetime.date(year, month, day)

    for i in boards_id:
        search_board(i)

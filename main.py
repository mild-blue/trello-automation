import requests
import json
import datetime
from my_secrets import TRELLO_KEY, TRELLO_TOKEN
from my_settings import BOARD_IDS, DEFAULT_TARGET_LIST_ID, MEMBER_NAME_ID_PAIRS, INPUT_LATEST_DUE_DATE


def make_trello_request(url_add_on: str, method: str = "GET", params: dict = None, data: dict = None):
    headers = {
        "Accept": "application/json"
    }
    url = f"https://api.trello.com/1/{url_add_on}"
    full_params = {'key': TRELLO_KEY, 'token': TRELLO_TOKEN}
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


def search_board(searched_board_id, target_list_id=DEFAULT_TARGET_LIST_ID):
    response = make_trello_request(f"boards/{searched_board_id}/lists")
    lists_on_board = json.loads(response.text)
    for searched_list in lists_on_board:
        if searched_list['id'] != target_list_id:
            search_list(searched_list['id'], target_list_id)


def search_list(searched_list_id, target_list_id=DEFAULT_TARGET_LIST_ID):
    response = make_trello_request(f"lists/{searched_list_id}/cards")
    cards_on_list = json.loads(response.text)
    for card in cards_on_list:
        for name in MEMBER_NAME_ID_PAIRS:
            if (MEMBER_NAME_ID_PAIRS[name] in card['idMembers']) and (check_due_date(card['id'])):
                copy_card(card['id'], target_list_id)


def copy_card(card_id, target_list_id):
    make_trello_request("cards",
                        method="POST",
                        params={"idList": target_list_id, "idCardSource": card_id}
                        )


def check_due_date(card_id):
    response = make_trello_request(f"cards/{card_id}/due")
    date_on_card_dict = json.loads(response.text)
    date_on_card = date_on_card_dict['_value']
    if date_on_card:
        card_date = datetime.datetime.strptime(date_on_card, "%Y-%m-%dT%H:%M:%S.%fZ").date()
        return card_date <= latest_due_date
    else:
        return False


if __name__ == '__main__':
    latest_due_date = datetime.date.today() + datetime.timedelta(days=NUMBER_OF_DAYS_TO_CONSUDER_IN_THE_SEARCH)
    for board_id in BOARD_IDS:
        search_board(board_id)
import requests
import json
import datetime
from datetime import datetime
from my_secrets import TRELLO_KEY, TRELLO_TOKEN
from my_settings import BOARD_IDS, DEFAULT_TARGET_LIST_ID, MEMBER_IDS, INPUT_LATEST_DUE_DATE


def make_trello_request(url: str, method: str = "GET", params: dict = None, data: dict = None):
    headers = {
        "Accept": "application/json"
    }
    full_url = f"https://api.trello.com/1/{url}"
    full_data = {'key': TRELLO_KEY, 'token': TRELLO_TOKEN}
    if data:
        full_data.update(data)
    response = requests.request(
        method,
        full_url,
        headers=headers,
        params=params,
        data=full_data
    )
    return response


def search_board(searched_board_id, target_list_id=DEFAULT_TARGET_LIST_ID):
    response = make_trello_request(f"boards/{searched_board_id}/lists")
    lists_on_board = json.loads(response.text)
    source_list_ids = []
    for searched_list in lists_on_board:
        if searched_list['id'] != target_list_id:
            source_list_ids.append(searched_list['id'])
    return source_list_ids


def search_list(searched_list_id, target_list_id=DEFAULT_TARGET_LIST_ID):
    response = make_trello_request(f"lists/{searched_list_id}/cards")
    cards_on_list = json.loads(response.text)
    source_card_ids = []
    for card in cards_on_list:
        for name in MEMBER_IDS:
            if (MEMBER_IDS[name] in card['idMembers']) and (check_due_date(card['id'])):
                source_card_ids.append(card['id'])
    return source_card_ids


def copy_card(card_id, target_list_id):
    make_trello_request("cards",
                        method="POST",
                        data={"idList": target_list_id, "idCardSource": card_id}
                        )


def check_due_date(card_id):
    response = make_trello_request(f"cards/{card_id}/due")
    date_on_card_dict = json.loads(response.text)
    date_on_card = date_on_card_dict['_value']
    if date_on_card:
        card_date = datetime.strptime(date_on_card, "%Y-%m-%dT%H:%M:%S.%fZ").date()
        return card_date <= latest_due_date
    else:
        return False


if __name__ == '__main__':
    latest_due_date = datetime.strptime(INPUT_LATEST_DUE_DATE, "%d.%m.%Y").date()
    all_source_list_ids = []
    for board_id in BOARD_IDS:
        all_source_list_ids = all_source_list_ids + search_board(board_id)
    all_source_card_ids = []
    for source_list_id in all_source_list_ids:
        all_source_card_ids = all_source_card_ids + search_list(source_list_id)
    for source_card_id in all_source_card_ids:
        copy_card(source_card_id, DEFAULT_TARGET_LIST_ID)

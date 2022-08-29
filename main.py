import requests
import json
import datetime
from requests import Response
from my_secrets import TRELLO_KEY, TRELLO_TOKEN
from my_settings import BOARD_IDS, DEFAULT_TARGET_LIST_ID, MEMBER_IDS, LATEST_DUE_DATE


def make_request(url: str, method: str = "GET", params: dict = None, data: dict = None) -> Response:
    headers = {
        "Accept": "application/json"
    }
    full_url = "https://api.trello.com/1/" + url
    full_params = {'key': TRELLO_KEY, 'token': TRELLO_TOKEN}
    if params:
        full_params.update(params)

    response = requests.request(
        method,
        full_url,
        headers=headers,
        params=full_params,
        data=data
    )
    return response


def search_board(searched_board_id: str, target_list_id=DEFAULT_TARGET_LIST_ID):
    response = make_request("boards/" + searched_board_id + "/lists")
    lists_on_board = json.loads(response.text)
    for searched_list in lists_on_board:
        if searched_list['id'] != target_list_id:
            search_list(searched_list['id'], target_list_id)


def search_list(searched_list_id: str, target_list_id=DEFAULT_TARGET_LIST_ID):
    response = make_request("lists/" + searched_list_id + "/cards")
    cards_on_list = json.loads(response.text)
    for card in cards_on_list:
        for name in MEMBER_IDS:
            if (MEMBER_IDS[name] in card['idMembers']) and (check_due_date(card['id'])):
                copy_card(card['id'], target_list_id)


def copy_card(card_id: str, target_list_id: str):
    make_request("cards",
                 method="POST",
                 params={"idList": target_list_id, "idCardSource": card_id}
                 )


def check_due_date(card_id: str) -> bool:
    response = make_request("cards/" + card_id + "/due")
    date_on_card = json.loads(response.text)
    unformatted_date = date_on_card['_value'].split('T')
    card_year, card_month, card_day = map(int, unformatted_date[0].split('-'))
    card_date = datetime.date(card_year, card_month, card_day)
    return card_date <= furthest_date


def print_id_of_my_boards(member_id: str):
    response_members = make_request("members/me")
    response_members_dict = json.loads(response_members.text)
    print("IDs of boards I'm a member of:")
    ids = response_members_dict["idBoards"]
    id_dictionary = {}
    for identity in ids:
        response_board = make_request("boards/" + identity)
        response_board_dict = json.loads(response_board.text)
        id_dictionary[response_board_dict["name"]] = identity
        print(response_board_dict["name"] + " - " + identity)


if __name__ == '__main__':
    day, month, year = map(int, LATEST_DUE_DATE.split('.'))
    furthest_date = datetime.date(year, month, day)
    for board in BOARD_IDS:
        search_board(board)

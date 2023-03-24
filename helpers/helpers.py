import datetime
import json

from my_settings import (LIST_IDS_TO_IGNORE,MEMBER_NAME_ID_PAIRS)
from helpers.trello_api import make_trello_request


def check_due_date(card_id: str, latest_due_date: datetime.date) -> bool:
    response = make_trello_request(f'cards/{card_id}/due')
    date_on_card_dict = json.loads(response.text)
    date_on_card = date_on_card_dict['_value']
    if date_on_card:
        card_date = datetime.datetime.strptime(date_on_card, '%Y-%m-%dT%H:%M:%S.%fZ').date()
        return card_date <= latest_due_date
    else:
        return False

def search_list(searched_list_id: str, latest_due_date: datetime.date, do_not_require_members_on_card: bool = False):
    response = make_trello_request(f'lists/{searched_list_id}/cards')
    cards_on_list = json.loads(response.text)
    source_card_ids = set()
    for card in cards_on_list:
        for name in MEMBER_NAME_ID_PAIRS:
            if (MEMBER_NAME_ID_PAIRS[name] in card['idMembers'] or do_not_require_members_on_card) and \
                    (check_due_date(card['id'], latest_due_date)) and \
                    (card['badges']['dueComplete'] is False):
                source_card_ids.add(card['id'])
    return source_card_ids


def get_list_cards_ids(list_id: str) -> list:
    response = make_trello_request(f'lists/{list_id}/cards')
    response_dict = json.loads(response.text)
    card_id_list = []
    for card in response_dict:
        card_id_list.append(card['id'])
    return card_id_list


def get_source_card_id(card_id: str) -> str:
    payload = {'filter': 'copyCard'}
    response = make_trello_request(f'cards/{card_id}/actions', params=payload)
    response_list = json.loads(response.text)
    if response_list:
        source_id = response_list[0]['data']['cardSource']['id']
        return source_id


def get_list_of_card_ids_previously_copied() -> list:
    target_list_card_ids = []
    for list_id in LIST_IDS_TO_IGNORE:
        target_list_card_ids.extend(get_list_cards_ids(list_id))
    copied_cards_ids = []
    for card_id in target_list_card_ids:
        copied_cards_ids.append(get_source_card_id(card_id))
    return copied_cards_ids


def get_name_id_pairs_of_my_boards():
    response_members = make_trello_request('members/me')
    response_members_dict = json.loads(response_members.text)
    print("IDs of boards I'm a member of:")
    ids = response_members_dict['idBoards']
    id_dictionary = {}
    for identity in ids:
        response_board = make_trello_request(f'boards/{identity}')
        response_board_dict = json.loads(response_board.text)
        id_dictionary[response_board_dict['name']] = identity
        print(response_board_dict['name'] + ' - ' + identity)
    return id_dictionary


def get_name_id_pairs_of_board_members(investigated_board_id: str) -> dict:
    members_json = make_trello_request(f'boards/{investigated_board_id}/members')
    members = json.loads(members_json.text)
    board_members_ids = {}
    for member in members:
        board_members_ids[member['fullName']] = member['id']
        print(member['fullName'] + ' - ' + member['id'])
    return board_members_ids


def get_board_list_name_id_pairs(investigated_board_id: str) -> dict:
    response = make_trello_request(f'boards/{investigated_board_id}/lists')
    lists_on_a_board_dict = json.loads(response.text)
    print('Name ID pairs of lists on a board', investigated_board_id)
    board_list_name_id_pairs_dict = {}
    for list_on_a_board in lists_on_a_board_dict:
        board_list_name_id_pairs_dict[list_on_a_board['name']] = list_on_a_board['id']
        print(list_on_a_board['name'] + ' - ' + list_on_a_board['id'])
    return board_list_name_id_pairs_dict

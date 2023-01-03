import datetime
import json

import requests

from my_secrets import TRELLO_KEY, TRELLO_TOKEN
from my_settings import (BOARD_IDS, DEFAULT_TARGET_LIST_ID,
                         IDS_OF_LISTS_TO_EXCLUDE, MEMBER_NAME_ID_PAIRS,
                         NUMBER_OF_DAYS_TO_CONSIDER_IN_THE_SEARCH)


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


def search_board(searched_board_id: int,
                 lists_to_exclude: list = IDS_OF_LISTS_TO_EXCLUDE):
    response = make_trello_request(f'boards/{searched_board_id}/lists')
    lists_on_board = json.loads(response.text)
    source_list_ids = []
    lists_to_exclude.append(DEFAULT_TARGET_LIST_ID)
    for searched_list in lists_on_board:
        if searched_list['id'] not in lists_to_exclude:
            source_list_ids.append(searched_list['id'])
    return source_list_ids


def search_list(searched_list_id: int, latest_due_date: datetime.date):
    response = make_trello_request(f'lists/{searched_list_id}/cards')
    cards_on_list = json.loads(response.text)
    source_card_ids = set()
    for card in cards_on_list:
        for name in MEMBER_NAME_ID_PAIRS:
            if (MEMBER_NAME_ID_PAIRS[name] in card['idMembers']) and \
                    (check_due_date(card['id'], latest_due_date)) and \
                    (card['badges']['dueComplete'] is False):
                source_card_ids.add(card['id'])
    return source_card_ids


def copy_card(card_id: str, target_list_id: str):
    response = make_trello_request('cards', method='POST', data={'idList': target_list_id, 'idCardSource': card_id})
    copy_checked_items_from_checklists(card_id, json.loads(response.text)['id'])


def check_due_date(card_id: str, latest_due_date: datetime.date) -> bool:
    response = make_trello_request(f'cards/{card_id}/due')
    date_on_card_dict = json.loads(response.text)
    date_on_card = date_on_card_dict['_value']
    if date_on_card:
        card_date = datetime.datetime.strptime(date_on_card, '%Y-%m-%dT%H:%M:%S.%fZ').date()
        return card_date <= latest_due_date
    else:
        return False


def get_target_list_card_ids() -> list:
    response = make_trello_request(f'lists/{DEFAULT_TARGET_LIST_ID}/cards')
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
    target_list_card_ids = get_target_list_card_ids()
    copied_cards_ids = []
    for id in target_list_card_ids:
        copied_cards_ids.append(get_source_card_id(id))
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


def sort_list_by_due_date(id_list: str, reverse=False) -> None:
    response = make_trello_request(f'lists/{id_list}/cards')
    cards = json.loads(response.text)
    id_due_date_dict = {}
    first_position = cards[0]['pos']
    for card in cards:
        if card['due']:
            id_due_date_dict[card['id']] = datetime.datetime.strptime(card['due'][0:10], '%Y-%m-%d')
        else:
            id_due_date_dict[card['id']] = None
    id_due_date_sorted_dict = sorted(id_due_date_dict.items(), key=lambda d: (d[1] is None, d[1]), reverse=reverse)

    position = first_position
    for id_due_date in id_due_date_sorted_dict:
        response = make_trello_request(f'cards/{id_due_date[0]}', params={'pos': f'{position}'}, method='PUT')
        position = position + first_position


def copy_checked_items_from_checklists(investigated_card_id: str, target_card_id: str):
    response_source = make_trello_request(f'cards/{investigated_card_id}/checklists')
    source_checklists_dict = json.loads(response_source.text)
    response_target = make_trello_request(f'cards/{target_card_id}/checklists')
    target_checklists_dict = json.loads(response_target.text)

    for checklist_source, checklist_target in zip(source_checklists_dict, target_checklists_dict):
        for check_item_source, check_item_target in zip(checklist_source['checkItems'], checklist_target['checkItems']):
            params = {'state': check_item_source['state']}
            make_trello_request(f'cards/{target_card_id}/checkItem/{check_item_target["id"]}',
                                method='PUT', params=params)


def copy_cards_with_tagged_members_and_close_due_date_to_list(latest_due_date: datetime.date):
    card_ids_previously_copied = get_list_of_card_ids_previously_copied()
    all_source_list_ids = []
    for board_id in BOARD_IDS:
        all_source_list_ids = all_source_list_ids + search_board(board_id)
    all_source_card_ids = set()
    for source_list_id in all_source_list_ids:
        all_source_card_ids.update(search_list(searched_list_id=source_list_id, latest_due_date=latest_due_date))
    for source_card_id in all_source_card_ids:
        if source_card_id not in card_ids_previously_copied:
            copy_card(source_card_id, DEFAULT_TARGET_LIST_ID)


def move_card(card_to_move_id: str, target_list_id: str):
    make_trello_request(f'cards/{card_to_move_id}', method='PUT', data={'idList': target_list_id})


def main():
    latest_due_date = datetime.date.today() + datetime.timedelta(days=NUMBER_OF_DAYS_TO_CONSIDER_IN_THE_SEARCH)
    copy_cards_with_tagged_members_and_close_due_date_to_list(latest_due_date)


if __name__ == '__main__':
    # get_name_id_pairs_of_my_boards()
    # get_name_id_pairs_of_board_members(BOARD_IDS[0])
    # get_board_list_name_id_pairs(BOARD_IDS[0])
    main()

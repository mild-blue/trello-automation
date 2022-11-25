import datetime
import json

import requests

from my_secrets import TRELLO_KEY, TRELLO_TOKEN
from my_settings import (BOARD_IDS, DEFAULT_TARGET_LIST_ID,
                         IDS_OF_LISTS_TO_EXCLUDE, LIST_IDS_TO_IGNORE,
                         LIST_IDS_TO_SORT, MEMBER_NAME_ID_PAIRS,
                         MOVE_FROM_LIST_IDS,
                         NUMBER_OF_DAYS_TO_CONSIDER_IN_THE_SEARCH)


class List:
    def __init__(self, list_id):
        self.id = list_id


class Card:
    def __init__(self, card_id, due_date, member_ids, completed):
        self.id = card_id
        self.due_date = due_date
        self.member_IDs = member_ids
        self.completed = completed


def parse_json_to_list(response: requests.models.Response, lists_to_exclude: list = IDS_OF_LISTS_TO_EXCLUDE):
    lists_on_board = json.loads(response.text)
    source_lists = []
    lists_to_exclude.append(DEFAULT_TARGET_LIST_ID)
    for searched_list in lists_on_board:
        if searched_list['id'] not in lists_to_exclude:
            source_lists.append(List(searched_list['id']))
    return source_lists


def parse_json_to_card(response: requests.models.Response):
    cards_on_list = json.loads(response.text)
    source_cards = []
    for card in cards_on_list:
        source_cards.append(Card(card_id=card['id'], due_date=card['badges']['due'], member_ids=card['idMembers'],
                         completed=card['badges']['dueComplete']))
    return source_cards


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
    source_lists = parse_json_to_list(response=response, lists_to_exclude=lists_to_exclude)
    return source_lists


def search_list(searched_list: List, latest_due_date: datetime.date):
    response = make_trello_request(f'lists/{searched_list.id}/cards')
    source_cards = parse_json_to_card(response=response)
    valid_source_cards = set()
    for card in source_cards:
        if not card.due_date:
            valid_source_cards.add(card)
        else:
            card_date = datetime.datetime.strptime(card.due_date, '%Y-%m-%dT%H:%M:%S.%fZ').date()
            for name in MEMBER_NAME_ID_PAIRS:
                if MEMBER_NAME_ID_PAIRS[name] in card.member_IDs and card_date <= latest_due_date and not card.completed:
                    valid_source_cards.add(card)
    return valid_source_cards


def copy_card(card: Card, target_list_id: str):
    response = make_trello_request("cards", method="POST", data={"idList": target_list_id, "idCardSource": card.id})
    copy_checked_items_from_checklists(card, json.loads(response.text)['id'])


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


def sort_list_by_due_date(id_list: str, reverse=False) -> None:
    response = make_trello_request(f'lists/{id_list}/cards')
    cards = json.loads(response.text)
    id_due_date_dict = {}
    first_position = cards[0]['pos']
    for card in cards:
        if card['due']:
            id_due_date_dict[card['id']] = datetime.datetime.strptime(card['due'][0:19], '%Y-%m-%dT%H:%M:%S')
        else:
            id_due_date_dict[card['id']] = None
    id_due_date_sorted_dict = sorted(id_due_date_dict.items(), key=lambda d: (d[1] is None, d[1]), reverse=reverse)

    position = first_position
    for id_due_date in id_due_date_sorted_dict:
        response = make_trello_request(f'cards/{id_due_date[0]}', params={'pos': f'{position}'}, method='PUT')
        position = position + first_position


def copy_checked_items_from_checklists(investigated_card: Card, target_card_id: str):
    response_source = make_trello_request('cards/' + investigated_card.id + '/checklists')
    source_checklists_dict = json.loads(response_source.text)
    response_target = make_trello_request(f'cards/{target_card_id}/checklists')
    target_checklists_dict = json.loads(response_target.text)

    for checklist_source, checklist_target in zip(source_checklists_dict, target_checklists_dict):
        for check_item_source, check_item_target in zip(checklist_source['checkItems'], checklist_target['checkItems']):
            params = {'state': check_item_source['state']}
            make_trello_request(f'cards/{target_card_id}/checkItem/{check_item_target["id"]}',
                                method='PUT', params=params)


def copy_cards_with_tagged_members_and_close_due_date_to_list(latest_due_date: datetime.date,
                                                              target_list_id: str = DEFAULT_TARGET_LIST_ID):
    card_ids_previously_copied = get_list_of_card_ids_previously_copied()
    all_source_list = []
    for board_id in BOARD_IDS:
        all_source_list = all_source_list + search_board(board_id)
    all_source_cards = set()
    for source_list in all_source_list:
        all_source_cards.update(search_list(searched_list_id=source_list, latest_due_date=latest_due_date))
    for source_card_id in all_source_cards:
        if source_card_id not in card_ids_previously_copied:
            copy_card(source_card_id, target_list_id)


def move_card(card_to_move_id: str, target_list_id: str):
    make_trello_request(f'cards/{card_to_move_id}', method='PUT', data={'idList': target_list_id})


def move_cards_with_close_due_date_between_lists(latest_due_date: datetime.date,
                                                 source_list_id: str, target_list_id: str):
    all_source_card_ids = search_list(searched_list_id=source_list_id, latest_due_date=latest_due_date,
                                      do_not_require_members_on_card=True)
    for source_card_id in all_source_card_ids:
        move_card(source_card_id, target_list_id)
        all_source_lists = all_source_lists + search_board(board_id)
    all_source_cards = set()
    for source_list in all_source_lists:
        all_source_cards.update(search_list(searched_list=source_list, latest_due_date=latest_due_date))
    for source_card in all_source_cards:
        copy_card(source_card, DEFAULT_TARGET_LIST_ID)


def main():
    latest_due_date = datetime.date.today() + datetime.timedelta(days=NUMBER_OF_DAYS_TO_CONSIDER_IN_THE_SEARCH)
    print('Starting to move cards.')
    for move_from_list_id in MOVE_FROM_LIST_IDS:
        move_cards_with_close_due_date_between_lists(latest_due_date=latest_due_date,
                                                     source_list_id=move_from_list_id,
                                                     target_list_id=DEFAULT_TARGET_LIST_ID)
    print('Moving cards complete. Starting to copy cards.')
    copy_cards_with_tagged_members_and_close_due_date_to_list(latest_due_date=latest_due_date)
    print('Copying cards complete. Starting to sort lists.')
    for sort_list_id in LIST_IDS_TO_SORT:
        sort_list_by_due_date(sort_list_id)


if __name__ == '__main__':
    # get_name_id_pairs_of_my_boards()
    # get_name_id_pairs_of_board_members(BOARD_IDS[0])
    # get_board_list_name_id_pairs(BOARD_IDS[0])
    main()

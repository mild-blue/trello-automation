import datetime
import json
from Card import Card
from TrelloList import TrelloList

from helper_functions.helpers import get_list_of_card_ids_previously_copied, parse_json_response_to_list_of_lists, search_list
from my_settings import (BOARD_IDS, DEFAULT_TARGET_LIST_ID,
                         IDS_OF_LISTS_TO_EXCLUDE)
from helper_functions.trello_api import make_trello_request


def search_board(searched_board_id: int, lists_to_exclude: list[str] = IDS_OF_LISTS_TO_EXCLUDE) -> list[TrelloList]:
    response = make_trello_request(f'boards/{searched_board_id}/lists')
    source_lists = parse_json_response_to_list_of_lists(response=response)
    lists_to_exclude.append(DEFAULT_TARGET_LIST_ID)
    source_lists = [source_list for source_list in source_lists if source_list.id not in lists_to_exclude]
    return source_lists


def copy_card(card_id: Card, target_list_id: str):
    response = make_trello_request('cards', method='POST', data={
        'idList': target_list_id, 'idCardSource': card_id})
    copy_checked_items_from_checklists(
        card_id, json.loads(response.text)['id'])


def copy_checked_items_from_checklists(investigated_card: Card, target_card_id: str):
    response_source = make_trello_request(f'cards/{investigated_card.id}/checklists')
    source_checklists_dict = json.loads(response_source.text)
    response_target = make_trello_request(f'cards/{target_card_id}/checklists')
    target_checklists_dict = json.loads(response_target.text)

    for checklist_source, checklist_target in zip(source_checklists_dict, target_checklists_dict):
        for check_item_source, check_item_target in zip(checklist_source['checkItems'], checklist_target['checkItems']):
            params = {'state': check_item_source['state']}
            make_trello_request(f'cards/{target_card_id}/checkItem/{check_item_target["id"]}',
                                method='PUT', params=params)


def copy_cards_with_tagged_members_and_close_due_date_to_list(latest_due_date: datetime.date,
                                                              target_list_id: str = DEFAULT_TARGET_LIST_ID) -> None:
    card_ids_previously_copied = get_list_of_card_ids_previously_copied()
    all_source_lists = []
    for board_id in BOARD_IDS:
        all_source_lists = all_source_lists + search_board(board_id)
    all_source_cards = set()
    for source_list in all_source_lists:
        all_source_cards.update(search_list(searched_list=source_list, latest_due_date=latest_due_date))
    for source_card in all_source_cards:
        if source_card.id not in card_ids_previously_copied:
            copy_card(source_card, target_list_id)

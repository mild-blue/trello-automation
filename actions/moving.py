import datetime

from helpers.helpers import search_list
from helpers.trello_api import make_trello_request


def move_card(card_to_move_id: str, target_list_id: str):
    make_trello_request(f'cards/{card_to_move_id}',
                        method='PUT', data={'idList': target_list_id})


def move_cards_with_close_due_date_between_lists(latest_due_date: datetime.date,
                                                 source_list_id: str, target_list_id: str):
    all_source_card_ids = search_list(searched_list_id=source_list_id, latest_due_date=latest_due_date,
                                      do_not_require_members_on_card=True)
    for source_card_id in all_source_card_ids:
        move_card(source_card_id, target_list_id)

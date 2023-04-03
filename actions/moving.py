import datetime

from Card import Card
from helpers.helpers import search_list
from helpers.trello_api import make_trello_request
from List import List


def move_card(card_to_move: Card, target_list_id: str) -> None:
    make_trello_request(f'cards/{card_to_move.id}', method='PUT', data={'idList': target_list_id})


def move_cards_with_close_due_date_between_lists(latest_due_date: datetime.date, source_list_id: str,
                                                 target_list_id: str) -> None:
    all_source_cards = set()
    all_source_cards.update(search_list(searched_list=List(source_list_id), latest_due_date=latest_due_date,
                                        do_not_require_members_on_card=True))
    for source_card in all_source_cards:
        move_card(source_card, target_list_id)

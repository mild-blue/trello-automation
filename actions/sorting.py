import datetime
import json

from helpers.trello_api import make_trello_request


def sort_list_by_due_date(id_list: str, reverse: bool = False) -> None:
    response = make_trello_request(f'lists/{id_list}/cards')
    cards = json.loads(response.text)
    id_due_date_dict = {}
    first_position = cards[0]['pos']
    for card in cards:
        if card['due']:
            id_due_date_dict[card['id']] = datetime.datetime.strptime(
                card['due'][0:19], '%Y-%m-%dT%H:%M:%S')
        else:
            id_due_date_dict[card['id']] = None
    id_due_date_sorted_dict = sorted(id_due_date_dict.items(
    ), key=lambda d: (d[1] is None, d[1]), reverse=reverse)

    position = first_position
    for id_due_date in id_due_date_sorted_dict:
        response = make_trello_request(
            f'cards/{id_due_date[0]}', params={'pos': f'{position}'}, method='PUT')
        position = position + first_position

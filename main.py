import requests
import json
import datetime
from secrets import *

mainEndpoint = "https://api.trello.com/1/"


def make_request(url: str, method: str = "GET", params: dict = None, data: dict = None):
    headers = {
        "Accept": "application/json"
    }
    full_params = {'key': trelloKey, 'token': trelloToken}
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


def search_board(board_id):
    response = make_request(mainEndpoint + "boards/" + board_id + "/lists")
    lists_on_board = json.loads(response.text)
    for list in lists_on_board:
        if list['id'] != newListID:
            search_list(list['id'])


def search_list(listID):
    response = make_request(mainEndpoint + "lists/" + listID + "/cards")
    cards_on_list = json.loads(response.text)
    for card in cards_on_list:
        for userID in membersID:
            if (userID in card['idMembers']) and (check_date(card['id'])):
                copy_card(card['id'], newListID)


def copy_card(card_id, listID):
    make_request(url=mainEndpoint + "cards",
                 method="POST",
                 params={"idList": listID, "idCardSource": card_id}
                 )


def check_date(card_id):
    response = make_request(mainEndpoint + "cards/" + card_id + "/due")
    date_on_card = json.loads(response.text)
    y = date_on_card['_value'].split('T')
    card_year, card_month, card_day = map(int, y[0].split('-'))
    card_date = datetime.date(card_year, card_month, card_day)
    return card_date <= end_date


if __name__ == '__main__':
    b = int(input("Enter number of boards you want to search:"))
    boardsID = []
    for i in range(b):
        boardStr = "Enter ID of board no." + str(i+1) + ":"
        boardsID.append(input(boardStr))
    newListID = input("Enter ID of a list you want to update:")
    n = int(input("Enter number of members you're searching for:"))
    membersID = []
    for i in range(n):
        memberStr = "Enter ID of member no. " + str(i + 1) + ":"
        membersID.append(input(memberStr))
    day, month, year = map(int, input("Furthest due date (Format: DD.MM.YYYY):").split('.'))
    end_date = datetime.date(year, month, day)

    for i in range(b):
        search_board(boardsID[i])

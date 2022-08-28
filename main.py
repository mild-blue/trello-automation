import requests
import json
import datetime
from secrets import *

mainEndpoint = "https://api.trello.com/1/"


def search_board(board_id):
    search_board_endpoint = mainEndpoint + "boards/" + board_id + "/lists"
    query_body = {"key": trelloKey, "token": trelloToken}
    response = requests.get(search_board_endpoint, json=query_body)
    lists_on_board = json.loads(response.text)
    for list in lists_on_board:
        if list['id'] != newListID:
            search_list(list['id'])


def make_request(url: str, method: str = "GET", data: dict = None):
    headers = {
        "Accept": "application/json"
    }
    params = {'key': trelloKey, 'token': trelloToken}

    response = requests.request(
        method,
        url,
        headers=headers,
        params=params,
        data=data
    )
    return response


def search_list(listID):
    query_body = {"key": trelloKey, "token": trelloToken}
    response = requests.get(mainEndpoint + "lists/" + listID + "/cards", json=query_body)
    cards_on_list = json.loads(response.text)
    for card in cards_on_list:
        for userID in membersID:
            if (userID in card['idMembers']) and (check_date(card['id'])):
                copy_card(card['id'], newListID)


def copy_card(card_id, listID):
    create_card_endpoint = mainEndpoint + "cards"
    json_obj = {"key": trelloKey, "token": trelloToken, "idList": listID, "idCardSource": card_id}
    requests.post(create_card_endpoint, json=json_obj)


def check_date(card_id):
    check_date_endpoint = mainEndpoint + "cards/" + card_id + "/due"
    query_body = {"key": trelloKey, "token": trelloToken}
    response = requests.get(check_date_endpoint, json=query_body)
    date_on_card = json.loads(response.text)
    y = date_on_card['_value'].split('T')
    card_year, card_month, card_day = map(int, y[0].split('-'))
    card_date = datetime.date(card_year, card_month, card_day)
    return card_date <= end_date


if __name__ == '__main__':
    boardID = input("Enter ID of a board you want to search:")
    newListID = input("Enter ID of a list you want to update:")
    n = int(input("Enter number of members you're searching for:"))
    membersID = []
    for i in range(n):
        memberStr = "Enter ID of member no. " + str(i+1) + ":"
        membersID.append(input(memberStr))
    day, month, year = map(int, input("Furthest due date (Format: DD.MM.YYYY):").split('.'))
    end_date = datetime.date(year, month, day)

    search_board(boardID)

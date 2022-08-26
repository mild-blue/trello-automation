import requests
import json

mainEndpoint = "https://api.trello.com/1/"
#trelloKey = "d4412efffa156d0b7366d851baf8433e"
#trelloToken = "8c5561b693898ea5ead94826d33d8ddf8dc8d36a2fa99be6f39fa3895f0f7693"
#newListID = "630796e26914d4004bd42044"
#boardID = "63077256a7d7e000935cead8"
#userID = "63075b03eb69dc0068756d79"

print("Enter Trello API key:")
trelloKey = input()
print("Enter Trello API token:")
trelloToken = input()
print("Enter ID of a board you want to search:")
boardID = input()
print("Enter ID of a list you want to update:")
newListID = input()
print("Enter number of members you're searching for:")
n = int(input())
membersID = []
for i in range(n):
    print("Enter ID of ", i+1, ". member")
    membersID.append(input())


def search_board(board_id):
    search_board_endpoint = mainEndpoint + "boards/" + board_id + "/lists"
    query_body = {"key": trelloKey, "token": trelloToken}
    response = requests.get(search_board_endpoint, json=query_body)
    lists_on_board = json.loads(response.text)
    for list in lists_on_board:
        if list['id'] != newListID:
            search_list(list['id'])


def search_list(listID):
    query_body = {"key": trelloKey, "token": trelloToken}
    response = requests.get(mainEndpoint + "lists/" + listID + "/cards", json=query_body)
    cards_on_list = json.loads(response.text)
    for card in cards_on_list:
        for userID in membersID:
            if userID in card['idMembers']:
                copy_card(card['id'], newListID)


def copy_card(card_id, listID):
    create_card_endpoint = mainEndpoint + "cards"
    json_obj = {"key": trelloKey, "token": trelloToken, "idList": listID, "idCardSource": card_id}
    requests.post(create_card_endpoint, json=json_obj)


search_board(boardID)

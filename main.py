import requests
import json

mainEndpoint = "https://api.trello.com/1/"
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

print("Furthest due date (Format: DD.MM.YYYY):")
x = input().split('.')
end_date = [int(x[2]), int(x[1]), int(x[0])]


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
    z = y[0].split('-')
    date = [int(z[0]), int(z[1]), int(z[2])]
    return compare(date, 0)


def compare(arr, j):
    if arr[j] < end_date[j]:
        return True
    elif arr[j] == end_date[j]:
        if j == 2:      # if the days are same too then include it too
            return True
        else:
            return compare(arr, j+1)
    else:
        return False


search_board(boardID)

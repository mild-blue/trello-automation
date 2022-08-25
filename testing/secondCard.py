import requests
import json

mainTrelloEndpoint = "https://api.trello.com/1/"
trelloKey = "d4412efffa156d0b7366d851baf8433e"
trelloToken = "8c5561b693898ea5ead94826d33d8ddf8dc8d36a2fa99be6f39fa3895f0f7693"
listID = "63077256a7d7e000935ceadf"


def create_card(card_name, card_desc):
    create_card_endpoint = mainTrelloEndpoint + "cards"
    jsonObj = {"key": trelloKey, "token": trelloToken, "idList": listID, "name": card_name, "desc": card_desc}
    newCard = requests.post(create_card_endpoint, json=jsonObj)

    print(json.loads(newCard.text))


create_card("Python card 2", "This is the second python card")
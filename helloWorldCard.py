import requests
import json

url = "https://api.trello.com/1/cards"

headers = {
   "Accept": "application/json"
}

query = {
   'idList': '63077256a7d7e000935ceadf',
   'key': 'd4412efffa156d0b7366d851baf8433e',
   'token': '8c5561b693898ea5ead94826d33d8ddf8dc8d36a2fa99be6f39fa3895f0f7693',
   'name': 'Hello world',
   'desc': 'This is a hello world card'
}

response = requests.request(
   "POST",
   url,
   headers=headers,
   params=query
)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))


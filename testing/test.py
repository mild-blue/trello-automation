import requests
import json

listID = "63077256a7d7e000935ceadf"
url = "https://api.trello.com/1/lists/" + listID + "/cards"

trelloKey = "d4412efffa156d0b7366d851baf8433e"
trelloToken = "8c5561b693898ea5ead94826d33d8ddf8dc8d36a2fa99be6f39fa3895f0f7693"

headers = {
   "Accept": "application/json"
}

query = {
   'key': trelloKey,
   'token': trelloToken
}

response = requests.request(
   "GET",
   url,
   headers=headers,
   params=query
)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

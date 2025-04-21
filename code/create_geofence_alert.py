import requests
import base64 
import json


username = "CART00101"
token = "fbb6811771992c8fdc38c2b967d15ff019842be4a9d77b4fb0ebaa546c0ef4b5"

auth = f"{username}:{token}"

auth_bytes = auth.encode('ascii')
base64_bytes = base64.b64encode(auth_bytes)
base64_auth = base64_bytes.decode('ascii')

url = "https://fleetapi-id.cartrack.com/rest/alerts/geofences"

payload=json.dumps({
    "name": "PICKUP_A ALERT",
    "registrations": [
        "ABC1234",
        "ABC5678"
    ],
    "geofence_trigger_id": 3, #3 is enters and leaves the geofences
    "geofence_ids": [
        "02870802-xxxx-42ed-xxxx-c999df353f42",
        "34589541-xxxx-73bc-xxxx-e821ed156f71"
    ],
    "geofence_group_ids": [
        12345,
        67891
    ],
    "contact_type": {
        "contact_type_id": 4, #contact type = 4 for send notification to alert center
        "values": [
            "john.doe@company.com",
            "johnny.doe@company.com"
        ],
        "priority_id": 1 #1 means high
    }
})
headers = {
    'Authorization': f'Basic {base64_auth}',
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
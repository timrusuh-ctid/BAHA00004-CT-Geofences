import requests
import base64 
import json

"""
Using your credentials
Please handle your credentials 
securely:

https://blog.logrocket.com/best-practices-for-managing-and-storing-secrets-in-frontend-development

We add them inline only for 
the purpose of this demonstration
"""

username = "CART00101"
token = "fbb6811771992c8fdc38c2b967d15ff019842be4a9d77b4fb0ebaa546c0ef4b5"

auth = f"{username}:{token}"

auth_bytes = auth.encode('ascii')
base64_bytes = base64.b64encode(auth_bytes)
base64_auth = base64_bytes.decode('ascii')

url = "https://fleetapi-id.cartrack.com/rest/geofences/groups"

payload=json.dumps({
    "name": "AWB-1-BAHA-TEST",
    "description": "B9017UEAFT",
    "subuser_id": ""
})

#GROUP ID FOR TEST GEOFENCES BAHA 00004 : 2761
headers = {
    'Authorization': f'Basic {base64_auth}',
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
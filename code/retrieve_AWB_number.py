import requests
import base64 

username = "CART00101"
token = "fbb6811771992c8fdc38c2b967d15ff019842be4a9d77b4fb0ebaa546c0ef4b5"

auth = f"{username}:{token}"

auth_bytes = auth.encode('ascii')
base64_bytes = base64.b64encode(auth_bytes)
base64_auth = base64_bytes.decode('ascii')

url = "https://fleetapi-id.cartrack.com/rest/geofences/groups?filter[name]=AWB"

payload={}
headers = {
    'Authorization': f'Basic {base64_auth}',
    'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
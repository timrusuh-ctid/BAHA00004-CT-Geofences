import requests
import base64 


username = "BAHA00004"
token = "9328ccf602f78bfdabef61a6f0d748f35559346bac09f49f94c41284240f8e4a"

auth = f"{username}:{token}"

auth_bytes = auth.encode('ascii')
base64_bytes = base64.b64encode(auth_bytes)
base64_auth = base64_bytes.decode('ascii')

url = "https://fleetapi-id.cartrack.com/rest/geofences"

payload={}
headers = {
    'Authorization': f'Basic {base64_auth}',
    'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
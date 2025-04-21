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

username = "BAHA00004"
token = "9328ccf602f78bfdabef61a6f0d748f35559346bac09f49f94c41284240f8e4a"

auth = f"{username}:{token}"

auth_bytes = auth.encode('ascii')
base64_bytes = base64.b64encode(auth_bytes)
base64_auth = base64_bytes.decode('ascii')

url = "https://fleetapi-id.cartrack.com/rest/geofences"

with open ('GEOFENCES\\JABODETABEK\\BEKASI\\BEKASI - CONVERTED\\WADMKC_Babelan_polygon_0.json','r') as file:
    polygon=json.load(file)
    #print(polygon)
#     polygon.append({
#         "name": "Cikarang Selatan",
#         "description":" Cikarang selatan via PY",
#         "colour": "#ce5239"
# })
payload=json.dumps(polygon)
headers = {
    'Authorization': f'Basic {base64_auth}',
    'Content-Type': 'application/json'
}


response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
import requests
import base64 
import json


username = "CART00101"
token = "fbb6811771992c8fdc38c2b967d15ff019842be4a9d77b4fb0ebaa546c0ef4b5"

auth = f"{username}:{token}"

auth_bytes = auth.encode('ascii')
base64_bytes = base64.b64encode(auth_bytes)
base64_auth = base64_bytes.decode('ascii')

url = "https://fleetapi-id.cartrack.com/rest/geofences"

# with open ('GEOFENCES\\JABODETABEK\\BEKASI\\BEKASI - CONVERTED\\WADMKC_Babelan_polygon_0.json','r') as file:
#     polygon=json.load(file)
    #print(polygon)
#     polygon.append({
#         "name": "Cikarang Selatan",
#         "description":" Cikarang selatan via PY",
#         "colour": "#ce5239"
# })
payload={
    "circle": { #for addresses
        "radius": 100,
        "longitude": 106.8182118, #RDTX Square -6.2176832,106.8182118
        "latitude": -6.2176 
        },
    "name": "PICKUP_A", #Location name
    "description": "RDTX Square",
    # "colour": "#ce5239",
    "geofence_group_ids":[
        #fill it with geofence_group_id that has name AWB number    
        2860 # 2860 : AWB12345TEST GROUP IN CART01001
    ]
}
headers = {
    'Authorization': f'Basic {base64_auth}',
    'Content-Type': 'application/json'
}


response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
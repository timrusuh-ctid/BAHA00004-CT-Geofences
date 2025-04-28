import requests
import base64
from pprint import pprint

# Authentication details
username = "CART00101"
token = "fbb6811771992c8fdc38c2b967d15ff019842be4a9d77b4fb0ebaa546c0ef4b5"

# Create base64 encoded authentication
auth = f"{username}:{token}"
auth_bytes = auth.encode('ascii')
base64_bytes = base64.b64encode(auth_bytes)
base64_auth = base64_bytes.decode('ascii')

# Filter parameters as variables 
date_from = "2025-01-01 00:00:00"
date_to = "2025-02-01 00:00:00" # can only be retrieved for 1 month
registration = ""  # Vehicle registration if needed
status = ""        # Alert status if needed
page = "1"         # Page number for pagination
limit = "100"      # Number of results per page
alert_type = "ZONE_ARRIVE_DEPART"    # Type of alert if needed

# Construct URL with filters
base_url = "https://fleetapi-id.cartrack.com/rest/alerts/notifications"
filters = f"?filter[date_from]={date_from}&filter[date_to]={date_to}"

# Add optional filters if they have values
if registration:
    filters += f"&filter[registration]={registration}"
if status:
    filters += f"&filter[status]={status}"
if page:
    filters += f"&page={page}"
if limit:
    filters += f"&limit={limit}"
if alert_type:
    filters += f"&filter[alert_type]={alert_type}"

url = base_url + filters

# API request
headers = {
    'Authorization': f'Basic {base64_auth}',
    'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data={})
pprint(response.text)
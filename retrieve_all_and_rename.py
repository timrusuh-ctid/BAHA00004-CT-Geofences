import requests
import base64
import json

def get_auth_header(username, token):
    """Generate the authorization header from credentials"""
    auth = f"{username}:{token}"
    auth_bytes = auth.encode('ascii')
    base64_bytes = base64.b64encode(auth_bytes)
    base64_auth = base64_bytes.decode('ascii')
    
    return {
        'Authorization': f'Basic {base64_auth}',
        'Content-Type': 'application/json'
    }

def get_filtered_geofences(username, token, name_prefix):
    """Retrieve geofences filtered by name prefix"""
    url = f"https://fleetapi-id.cartrack.com/rest/geofences?limit=200&filter[name]={name_prefix}"
    headers = get_auth_header(username, token)
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching geofences: {response.status_code}")
        print(response.text)
        return None
    
    # Parse the response
    geofence_data = response.json().get('data', [])
    
    # Create a simplified list with only id and name
    simplified_geofences = [
        {"geofence_id": geofence["geofence_id"], "name": geofence["name"]}
        for geofence in geofence_data
    ]
    
    return simplified_geofences

def update_geofence_name(username, token, geofence_id, current_name, prefix_to_remove):
    """Update a geofence name by removing the specified prefix"""
    # Ensure the name starts with the prefix before removing
    if current_name.startswith(prefix_to_remove):
        new_name = current_name[len(prefix_to_remove):]
        
        # Prepare update data with new name
        update_data = {
            "name": new_name
        }
        
        url = f"https://fleetapi-id.cartrack.com/rest/geofences/{geofence_id}"
        headers = get_auth_header(username, token)
        
        response = requests.put(url, headers=headers, json=update_data)
        if response.status_code in [200, 201, 204]:
            print(f"Successfully updated geofence: {current_name} → {new_name}")
            return True
        else:
            print(f"Error updating geofence {geofence_id}: {response.status_code}")
            print(response.text)
            return False
    else:
        print(f"Geofence name '{current_name}' does not start with prefix '{prefix_to_remove}'")
        return False

def main():
    # Your credentials
    username = "BAHA00004"
    token = "9328ccf602f78bfdabef61a6f0d748f35559346bac09f49f94c41284240f8e4a"
    
    # The prefix to filter and remove
    prefix = "WADMKC_"
    
    # Get geofences filtered by the prefix
    filtered_geofences = get_filtered_geofences(username, token, prefix)
    
    if filtered_geofences:
        print(f"Found {len(filtered_geofences)} geofences with prefix '{prefix}'")
        
        # Save the filtered data to a file
        with open('filtered_geofences.json', 'w') as f:
            json.dump(filtered_geofences, f, indent=2)
        
        # Process each geofence to remove the prefix
        success_count = 0
        for geofence in filtered_geofences:
            if update_geofence_name(username, token, geofence["geofence_id"], 
                                   geofence["name"], prefix):
                success_count += 1
        
        print(f"Successfully updated {success_count} out of {len(filtered_geofences)} geofences")
    else:
        print(f"No geofences found with prefix '{prefix}'")

if __name__ == "__main__":
    main()
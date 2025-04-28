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

def get_geofences_by_description(username, token, description):
    """Retrieve geofences filtered by description"""
    url = f"https://fleetapi-id.cartrack.com/rest/geofences?limit=200&filter[description]={description}"
    headers = get_auth_header(username, token)
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching geofences: {response.status_code}")
        print(response.text)
        return None
    
    # Parse the response
    geofence_data = response.json().get('data', [])
    
    # Create a simplified list with id, name, and description
    simplified_geofences = [
        {
            "geofence_id": geofence["geofence_id"], 
            "name": geofence["name"],
            "description": geofence.get("description", "")
        }
        for geofence in geofence_data
    ]
    
    return simplified_geofences

def update_geofence_description(username, token, geofence_id, name, current_description, new_description):
    """Update a geofence description only"""
    # Prepare update data with only the description
    update_data = {
        "description": new_description
    }
    
    url = f"https://fleetapi-id.cartrack.com/rest/geofences/{geofence_id}"
    headers = get_auth_header(username, token)
    
    response = requests.put(url, headers=headers, json=update_data)
    if response.status_code in [200, 201, 204]:
        print(f"Successfully updated geofence '{name}': description '{current_description}' → '{new_description}'")
        return True
    else:
        print(f"Error updating geofence {geofence_id}: {response.status_code}")
        print(response.text)
        return False

def main():
    # Your credentials
    username = "BAHA00004"
    token = "9328ccf602f78bfdabef61a6f0d748f35559346bac09f49f94c41284240f8e4a"  # Replace with actual token
    
    # The description to filter by
    filter_description = "TEST"
    
    # The new description to set
    new_description = "Kecamatan"
    
    # Get geofences filtered by description
    filtered_geofences = get_geofences_by_description(username, token, filter_description)
    
    if filtered_geofences:
        print(f"Found {len(filtered_geofences)} geofences with description '{filter_description}'")
        
        # Save the filtered data to a file
        with open('description_filtered_geofences.json', 'w') as f:
            json.dump(filtered_geofences, f, indent=2)
        
        # Process each geofence to update description only
        success_count = 0
        for geofence in filtered_geofences:
            if update_geofence_description(
                username, 
                token, 
                geofence["geofence_id"],
                geofence["name"],
                geofence["description"], 
                new_description
            ):
                success_count += 1
        
        print(f"Successfully updated {success_count} out of {len(filtered_geofences)} geofences")
    else:
        print(f"No geofences found with description '{filter_description}'")

if __name__ == "__main__":
    main()
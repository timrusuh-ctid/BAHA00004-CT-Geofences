import requests
import base64 
import json
from pathlib import Path
import time

def setup_auth():
    username = "BAHA00004"
    token = "9328ccf602f78bfdabef61a6f0d748f35559346bac09f49f94c41284240f8e4a"
    
    auth = f"{username}:{token}"
    auth_bytes = auth.encode('ascii')
    base64_bytes = base64.b64encode(auth_bytes)
    base64_auth = base64_bytes.decode('ascii')
    
    return base64_auth

def post_geofence(file_path, base64_auth):
    url = "https://fleetapi-id.cartrack.com/rest/geofences"
    
    try:
        with open(file_path, 'r') as file:
            polygon = json.load(file)
        
        payload = json.dumps(polygon)
        headers = {
            'Authorization': f'Basic {base64_auth}',
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        
        print(f"Processing {file_path.name}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        print("-" * 50)
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def batch_post_geofences(folder_path):
    # Setup authentication
    base64_auth = setup_auth()
    
    # Get all JSON files in the folder
    folder = Path(folder_path)
    json_files = list(folder.glob('*.json'))
    
    print(f"Found {len(json_files)} JSON files to process")
    
    successful_posts = 0
    failed_posts = 0
    
    # Process each file
    for file_path in json_files:
        # Add a delay between requests to avoid overwhelming the API
        if successful_posts > 0 or failed_posts > 0:
            time.sleep(1)  # 1 second delay between requests
            
        if post_geofence(file_path, base64_auth):
            successful_posts += 1
        else:
            failed_posts += 1
    
    # Print summary
    print("\nSummary:")
    print(f"Total files processed: {len(json_files)}")
    print(f"Successful posts: {successful_posts}")
    print(f"Failed posts: {failed_posts}")

if __name__ == "__main__":
    folder_path = "GEOFENCES\\Geojson_jawabarat\\jawabarat-CONVERTED"
    batch_post_geofences(folder_path)
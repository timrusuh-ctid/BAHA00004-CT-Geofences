import json
import pandas as pd
import datetime
now = datetime.datetime.now().strftime('%Y%m%d')

# Load JSON file
with open('GEOFENCES\\JABODETABEK\\BEKASI\\BEKASI\\WADMKC_Cikarang Selatan.geojson', 'r') as f: 
    data = json.load(f)

# Prepare data for DataFrame
time = now + '01'
rows = []
geofenceName = data['name']
for feature in data['features']:
    geofence_name = geofenceName
    geofence_description = 'Geofence Testing'
    
    # Extract and format coordinates
    coordinates = feature['geometry']['coordinates']
    formatted_points = []
    for multi_polygon in coordinates:
        for polygon in multi_polygon:
            for point in polygon:
                lat, long = point[1], point[0]  # Swap to LAT#LONG format
                
                formatted_points.append(f'{lat}#{long}')
    
    points = '#'.join(formatted_points)
    newCoordinates=points.split('#')
    newPolygon = []
    for i in range(0, len(newCoordinates), 2):
            # Get latitude and longitude
            latitude = float(newCoordinates[i])
            longitude = float(newCoordinates[i+1])
            
            # Add to polygon array
            newPolygon.append({
                "lat":latitude,
                "lng":longitude
            })
    

    #print (newPolygon)
    # Append row data
    rows.append([geofence_name, geofence_description, points, '', ''])
    #print(newPolygon)

    #print(json_result)
    #json.dumps({"polygon": newPolygon}, indent=2)
# Create DataFrame
df = pd.DataFrame(rows, columns=['Geofence Name', 'Geofence Description', 'Point(Lat#Lon#Lat#Lon...)', 'Group Name', 'Group Description'])
#print (df.head)

# Save to Excel
#fileName = f'GEOFENCES\\{geofenceName}-{time}.csv'
#df.to_csv(fileName, index=False)

#print(f"Excel file has been created: {fileName}")


with open('cikarang_selatan.json','w') as f:
    results={"polygon":newPolygon}
    json_results=json.dumps(results,indent=2)
    f.write(json_results)
from pathlib import Path
import os
import json
#import pandas as pd
import datetime
now = datetime.datetime.now().strftime('%Y%m%d')


def process_single_file(file_path, output_folder):
    try:
        # Read the GeoJSON file
        with open(file_path, 'r') as f:
            geojson_data = json.load(f)
        
        area_name = file_path.stem
        # Remove WADMKC_ prefix if present  
        folder_path = str(file_path.parent)
        if "JawaTengah" in folder_path:
            geofence_group_ids = 2776
            area_description = "Kecamatan di Jawatengah"
        elif "JawaTimur" in folder_path:
            geofence_group_ids = 2777
            area_description = "Kecamatan di Jawatimur"
        else:
            geofence_group_ids = 2775  # default value
            area_description = "Kecamatan di Jawabarat"  # default value

    
        polygon_count = 0
        
        # Process each feature in the GeoJSON
        for feature in geojson_data.get('features', []):
            geometry = feature.get('geometry', {})
            
            if geometry['type'] in ['Polygon', 'MultiPolygon']:
                # Get coordinates based on geometry type
                if geometry['type'] == 'Polygon':
                    polygons = [geometry['coordinates'][0]]  # Single polygon
                else:
                    polygons = [poly[0] for poly in geometry['coordinates']]  # Multiple polygons
                
                # Process each polygon
                total_polygons = len(polygons)
                for idx, coords in enumerate(polygons):
                    # Convert coordinates to required format
                    polygon = [
                        {"lat": coord[1], "lng": coord[0]} 
                        for coord in coords
                    ]
                    
                    # Create output filename
                    base_name = file_path.stem
                    if base_name.startswith("WADMKC_"):
                        base_name = base_name[len("WADMKC_"):]
                    
                    # Add number suffix only if there are multiple polygons
                    if total_polygons > 1:
                        polygon_name = f"{base_name}_{idx + 1}"
                        output_file = output_folder / f"{file_path.stem}_{idx + 1}.json"
                    else:
                        polygon_name = base_name
                        output_file = output_folder / f"{file_path.stem}.json"
                    #create complete output data structure
                    output_data={
                        "polygon": polygon,
                        "name": polygon_name,
                        "geofence_group_ids" : geofence_group_ids,
                        "description":area_description
                    }

                    # Save polygon to file
                    with open(output_file, 'w') as f:
                        json.dump(output_data, f, indent=2)
                    
                    print(f"Saved: {output_file}")
                    polygon_count += 1
        
        return polygon_count
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0
def batch_process_folder(input_folder, output_folder):
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    
    # Create output folder
    os.makedirs(output_path, exist_ok=True)
    
    # Find all GeoJSON files
    geojson_files = list(input_path.glob('**/*.geojson'))
    print(f"Found {len(geojson_files)} GeoJSON files")
    
    total_polygons = 0
    processed_files = 0
    
    # Process each file
    for file_path in geojson_files:
        print(f"\nProcessing: {file_path}")
        polygons_saved = process_single_file(file_path, output_path)
        
        if polygons_saved > 0:
            processed_files += 1
            total_polygons += polygons_saved
            
    print(f"\nComplete! Processed {processed_files} files, saved {total_polygons} polygons")


if __name__ == "__main__":
    # Replace these paths with your actual folder paths
    input_folder = "GEOFENCES\\JawaTimur-Exported\\JawaTimur-Exported"
    output_folder = "GEOFENCES\\JawaTimur-Exported\\JawaTimur-Converted"
    # Call the batch process function
    
    batch_process_folder(input_folder, output_folder)

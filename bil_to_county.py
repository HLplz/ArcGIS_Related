import arcpy
import os

# Define the folder path containing the .bil files
folder_path = ## folder where all .bil files are stored

# Define the shapefile for zoning (adjust path as needed)
shapefile = ## shapfile
# Output folder for the resulting .csv files
output_folder = os.path.join(folder_path, "Results")

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Iterate through all .bil files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.bil'): #subject to change based on data in the folder 
        # Full path to the .bil file
        bil_file = os.path.join(folder_path, file_name)
        
        # Generate a name for the raster layer
        raster_layer_name = os.path.splitext(os.path.basename(bil_file))[0]
        
        # Create Raster Layer from the .bil file
        raster_layer = arcpy.MakeRasterLayer_management(
            bil_file, 
            raster_layer_name
        )
        
        # Generate output .csv name based on the raster file name
        csv_file_name = f"{raster_layer_name}_output.csv"
        csv_file_path = os.path.join(output_folder, csv_file_name)
        
        # Perform Zonal Statistics and output to an in-memory table
        zonal_table = arcpy.sa.ZonalStatisticsAsTable(
            in_zone_data=shapefile, 
            zone_field="GEOID",  # Adjust this field based on your shapefile
            in_value_raster=raster_layer, 
            out_table="in_memory/zonal_table",  # Use in-memory workspace
            statistics_type="MEAN"
        )
        
        # Check if the in-memory table was created successfully
        if arcpy.Exists(zonal_table):
            # Export the in-memory table to CSV
            arcpy.TableToTable_conversion(
                zonal_table, 
                output_folder, 
                csv_file_name
            )
            
            # Rename the .csv file if needed (for example, adding a prefix or suffix)
            new_csv_file_name = ## subject to change
            new_csv_file_path = os.path.join(output_folder, new_csv_file_name)
            os.rename(csv_file_path, new_csv_file_path)
            
            # Print confirmation
            print(f"Processed: {new_csv_file_name}")
        else:
            print(f"Error: Zonal statistics table not created for {raster_layer_name}")


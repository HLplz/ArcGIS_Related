import arcpy
import os


folder_path = ## folder where all .bil data stored

# .shp file path: can be county level or other geo division
shapefile = r"C:\Users\haiyu\OneDrive\Desktop\UNMC\231119_PM2.5\CONUS_counties_2016\CONUS_counties_2016.shp"

# result folder
output_folder = os.path.join(folder_path, "Results")
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# produce .csv files from .bil files
for file_name in os.listdir(folder_path):
    if file_name.endswith('.bil'):
        try:
            bil_file = os.path.join(folder_path, file_name)
            
            # Check if the file exists
            if not os.path.exists(bil_file):
                print(f"File does not exist: {bil_file}")
                continue
            
            # generate raster layer based on .bil file
            raster_layer_name = os.path.splitext(os.path.basename(bil_file))[0]
            
            raster_layer = arcpy.MakeRasterLayer_management(
                bil_file, 
                raster_layer_name
            )
            
            # name the output raster (optional)
            csv_file_name = f"{raster_layer_name}_output.csv"
            csv_file_path = os.path.join(output_folder, csv_file_name)
            
            # zonal stats
            zonal_table = arcpy.sa.ZonalStatisticsAsTable(
                in_zone_data=shapefile, 
                zone_field="GEOID",  # adjust based on your geo division, mine is US county so GEOID
                in_value_raster=raster_layer, 
                out_table="in_memory/zonal_table",  
                statistics_type="ALL" # adjust based on what you need, e.g. "MEAN" "MAX"
            )
            
            if arcpy.Exists(zonal_table):
                # Export the in-memory table to CSV
                arcpy.TableToTable_conversion(
                    zonal_table, 
                    output_folder, 
                    csv_file_name
                )
                
                new_csv_file_name = ## name your output .csv file 
                new_csv_file_path = os.path.join(output_folder, new_csv_file_name)
                os.rename(csv_file_path, new_csv_file_path)
                
                # Print confirmation
                print(f"Processed: {new_csv_file_name}")
            else:
                print(f"Error: Zonal statistics table not created for {raster_layer_name}")
                
        except arcpy.ExecuteError as e:
            # Handle specific ArcPy errors
            print(f"ArcPy error processing {raster_layer_name}: {e}")
        except Exception as e:
            # Handle other possible errors
            print(f"General error processing {raster_layer_name}: {e}")

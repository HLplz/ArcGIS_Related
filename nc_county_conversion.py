import arcpy
from arcpy.sa import *
import netCDF4
import os

# Set the workspace and environment settings

arcpy.env.workspace = #workspace folder path
arcpy.env.overwriteOutput = True

shapefile = # .shp file that defines geographical division

# extract all .nc file in data folder
# to be revised based on file type
nc_list = []
folder_path = #folder path
for file_name in os.listdir(folder_path):
    #print(file_name)
    if '.nc' in file_name and '.aux' not in file_name:
        nc_list.append(file_name)
print(nc_list[0:5])

# variables of interest
variables = # list of variables of interest 

# Load the NetCDF File and Extract Variables
netcdf_file_path = ## path to data folder 

for file in nc_list:
    print('processing: ' + file)

    netcdf_file = netcdf_file_path + file


    raster_layers = []

    for var in variables:
        raster_layer = arcpy.md.MakeNetCDFRasterLayer(
            netcdf_file,
            var,                # Var name
            "lon",              # may be LON/Lon or others depending on your .nc file
            "lat",              # may be LAT/Lat or others depending on your .nc file
            var,                # Output Raster Layer name
            band_dimension="",
            dimension_values="",
            value_selection_method="BY_VALUE"
        )
        raster_layers.append(raster_layer)


    output_folder = #output path 
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, raster_layer in enumerate(raster_layers):
        output_table = os.path.join(output_folder, f"Variable_{variables[i]}.dbf")

        arcpy.sa.ZonalStatisticsAsTable(
            in_zone_data=shapefile,
            zone_field="GEOID",  # Adjust this field if needed based on your shapefile
            in_value_raster=raster_layer,
            out_table=output_table,
            statistics_type="ALL"
        )

    ## csv_file_name is subject to change 
    for i, raster_layer in enumerate(raster_layers):
        dbf_table = os.path.join(output_folder, f"Variable_{variables[i]}.dbf")
        csv_file_name = netcdf_file[-13:-7] + f"_{variables[i]}.csv"
        csv_file = os.path.join(output_folder, csv_file_name)

        if arcpy.Exists(dbf_table):
            arcpy.TableToTable_conversion(dbf_table, output_folder, csv_file_name)
        else:
            print("dff doesn't exist or dbf error")

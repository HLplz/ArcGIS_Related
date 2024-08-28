import arcpy
from arcpy import env
from arcpy.sa import *
import os
import pandas as pd

arcpy.env.addOutputsToMap = False 
variables = ['sfsm_inst','gws_inst', 'rtzsm_inst'] # input your variables of concern 

netcdf_file_path = # your .nc folder path
shapefile = # your shapefile 

nc_list = [f for f in os.listdir(netcdf_file_path) if f.endswith('.nc4')]


for file in nc_list:
    print(file) # track progress 
    filename_without_extension = os.path.splitext(file)[0]
    netcdf_full_path = os.path.join(netcdf_file_path, file)

    for var in variables:
        last_nine = filename_without_extension[-12:-4]
        raster_layer = arcpy.md.MakeNetCDFRasterLayer(
            netcdf_full_path,        
            var,                # Var name
            "lon",              # may be LON/Lon or others depending on your .nc file
            "lat",              # may be LAT/Lat or others depending on your .nc file
            f'{last_nine}_{var}',                # Output Raster Layer name
            band_dimension="", 
            dimension_values="", 
            value_selection_method="BY_VALUE"
        )
        output_tiff = os.path.join(netcdf_file_path, f'{last_nine}_{var}.tif')
        arcpy.management.CopyRaster(raster_layer[0], output_tiff, '', None, '-999', 'NONE', 'NONE', '', 'NONE', 'NONE', 'TIFF', 'NONE', 'CURRENT_SLICE', 'NO_TRANSPOSE')

        output_table = os.path.join(netcdf_file_path, f'{last_nine}_{var}.dbf')

        arcpy.sa.ZonalStatisticsAsTable(
            in_zone_data=shapefile, 
            zone_field="GEOID",  # Adjust this field if needed based on your shapefile
            in_value_raster=output_tiff, 
            out_table=output_table, 
            statistics_type="MEAN"
        )
        output_folder = # your output folder 
        output_excel = os.path.join(output_folder, f'{last_nine}_{var}.xls')
        arcpy.TableToExcel_conversion(output_table, output_excel)
        
        output_csv = os.path.join(output_folder, f'{last_nine}_{var}.csv')
        df = pd.read_excel(output_excel)
        df.to_csv(output_csv, index=False)
        # Cleanup if wrriten into env
        arcpy.Delete_management(output_tiff)
        arcpy.Delete_management(output_table)
        arcpy.Delete_management(output_excel)
        #arcpy.Delete_management(output_csv)
        #arcpy.Delete_management(csv_file_name)
        arcpy.Delete_management(raster_layer)
        arcpy.Delete_management('in_memory')


# Lab 4 - Buffer and Intersect Exercise

import arcpy

#Define our Workspace
arcpy.env.workspace = r"M:\Staff Folders\Ben Strickland\TAMU\ArcProPython\Lab4"
folder_path = r"M:\Staff Folders\Ben Strickland\TAMU\ArcProPython\Lab4\Lab4_FunWithArcPy"
gdb_name = 'Campus.gdb'
gdb_path = folder_path + '\\' + gdb_name

# Create geodatabase
arcpy.CreateFileGDB_management(folder_path, gdb_name)

print("Geodatabase Created")

# Path to CSV file we are using
csv_path = r"M:\Staff Folders\Ben Strickland\TAMU\ArcProPython\Lab4\Lab4_FunWithArcPy\garages.csv"
garage_layer_name = "Garage_Points"
garages = arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', garage_layer_name)



input_layer = garages
arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
garage_points = gdb_path + '\\' + garage_layer_name

print("Garages Points Created")

# Copy feature class to our workspace geodatabase from another geodatabase
campus = r"M:\Staff Folders\Ben Strickland\TAMU\ArcProPython\Campus.gdb"
buildings_campus = campus + '\Structures'
buildings = gdb_path + '\\' + 'Buildings'


arcpy.Copy_management(buildings_campus, buildings)

print("Feature Classes Imported")


# Reporject our Garage Points
spatial_ref = arcpy.Describe(buildings).spatialReference
arcpy.Project_management(garage_points, gdb_path + '\Garage_Points_Reprojected', spatial_ref)

print("Points Reprojected")

#Buffer the Garages
garageBuffer = arcpy.Buffer_analysis(gdb_path + '\Garage_Points_Reprojected', gdb_path + '\Garage_Points_Buffer', 150)

print("Buffer Created")

# Intersect our Garage Buffer with Campus Buildings
arcpy.Intersect_analysis([garageBuffer, buildings], gdb_path + '\Garage_Building_Intersect', 'ALL')

print("Intersect Created")

# New table now in our working folder
arcpy.TableToTable_conversion(gdb_path + '\Garage_Building_Intersect.dbf', folder_path, 'BuildingsCloseBy.csv')

print("Table Created")

print("Lab 4 Finished")
















# GIS Programming 
# GEOG 676
# Lab 4


# Define our Workspace and Geodatabase

- This portion is the setting of our **workspace** and **folder path**. Once this is set, 
then we create our **Geodatabase** or **GDB**, which is called **Campus**.

- The variables created give us our workspace, our folder we are saving our work in, 
our geodatabase that we will save our feature classes in, and our path to that geodatabase.

```python
import arcpy

# Define our Workspace
arcpy.env.workspace = r"M:\Staff Folders\Ben Strickland\TAMU\ArcProPython\Lab4"
folder_path = r"M:\Staff Folders\Ben Strickland\TAMU\ArcProPython\Lab4\Lab4_FunWithArcPy"
gdb_name = 'Campus.gdb'
gdb_path = folder_path + '\\' + gdb_name

# Create geodatabase
arcpy.CreateFileGDB_management(folder_path, gdb_name)

print("Geodatabase Created")
```

# Path to CSV file

- We then will create our garage points with the help of our csv file, **garages.csv**.
Once this conversion is successful, we then input this layer into our **Campus.gdb**.


```python
# Path to CSV file we are using
csv_path = r"M:\Staff Folders\Ben Strickland\TAMU\ArcProPython\Lab4\Lab4_FunWithArcPy\garages.csv"
garage_layer_name = "Garage_Points"
garages = arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', garage_layer_name)



input_layer = garages
arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
garage_points = gdb_path + '\\' + garage_layer_name

print("Garages Points Created")
```

# Copy feature class to our current workspace

- In previous weeks, we have used another geodatabase, campus.gdb, with feature classes that we would now like to use in our current workspace. 

- To do this, we need import a feature class, **Structures**, from our previously used campus.gdb, to our current **Campus** geodatabase, and name it **Buildings**.

```python
# Copy feature class to our workspace geodatabase from another geodatabase
campus = r"M:\Staff Folders\Ben Strickland\TAMU\ArcProPython\Campus.gdb"
buildings_campus = campus + '\Structures'
buildings = gdb_path + '\\' + 'Buildings'


arcpy.Copy_management(buildings_campus, buildings)

print("Feature Classes Imported")
```

# Reporject our Garage Points

- Out next step is to reproject our **Garage_Points**.

```python
# Reporject our Garage Points
spatial_ref = arcpy.Describe(buildings).spatialReference
arcpy.Project_management(garage_points, gdb_path + '\Garage_Points_Reprojected', spatial_ref)

print("Points Reprojected")
```

# Buffer and Intersect

- Our next set is to use some of our basic operations we have learned, which is the **Buffer** and **Intersect** tool. We are going to create a buffer around our Garage Points, and then see which buildings intersect within the given distance.


```python
# Buffer the Garages
garageBuffer = arcpy.Buffer_analysis(gdb_path + '\Garage_Points_Reprojected', gdb_path + '\Garage_Points_Buffer', 150)

print("Buffer Created")

# Intersect our Garage Buffer with Campus Buildings
arcpy.Intersect_analysis([garageBuffer, buildings], gdb_path + '\Garage_Building_Intersect', 'ALL')

print("Intersect Created")
```

# Table creation from our Intersect feature class

- Now that we have **Garage_Building_Intersect** feature class, we now want to a csv to show which buildings intersect within the given distance. To do this, we use a **TableToTable** conversion. Once this is done, we are finished!

```python
# New table now in our working folder
arcpy.TableToTable_conversion(gdb_path + '\Garage_Building_Intersect.dbf', folder_path, 'BuildingsCloseBy.csv')

print("Table Created")

print("Lab 4 Finished")
```




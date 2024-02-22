# GIS Programming 
# GEOG 676
# Lab 5

# Creating a toolbox

- In this lab, we are creating a **toolbox**. This toolbox will perfect a task that we had previously performed in Lab 4 - Fun with ArcPy. 

- We will now perform those same tasks, but now we will create a tool where we can input parameters from our **GDB**.

- When we open ArcPro, we will navigate to our **ArcCatalog** tab on the right hand side and right-click **Toolboxes** and select **New Python Tool**. We will name the tool and save it into our working folder. Once this is done, we refresh that same **Toolboxes** tab, refresh it, and we now see our newly created toolbox. 

- When we click the arrow down, we see a script automatically created by Arc. We right click and edit, and we now see this default script ready for us to edit.

```python
import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):                                                     
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Building Proximity"
        self.description = "Determines what buildings are near targeted building"
        self.canRunInBackground = False
        self.category = "Building Tools"
```
- This area, **getParameters** is our main area of focus as we input our edits to this script. We want our user to be able to input a **GDB Folder**, **GDB Name**, **CSV File**, **Layer Name**, and the original  **Campus GDB**. These are the parameters needed for the process of our Garage points to be created from our csv file, our buildings to be moved to our current GDB, and our Garage points to have a buffer.

```python
    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName= "GDB Folder",
            name= "GDB Folder",
            datatype= "DEFolder",
            parameterType= "Required",
            direction= "Input"
        )
        param1 = arcpy.Parameter(
            displayName= "GDB Name",
            name= "GDB Name",
            datatype= "GPStirng",
            parameterType= "Required",
            direction= "Input"
        )
        param2 = arcpy.Parameter(
            displayName= "Garage CSV File",
            name= "Garage CSV File",
            datatype= "DEFile",
            parameterType= "Required",
            direction= "Input"
        )
        param3 = arcpy.Parameter(
            displayName= "Garage Layer Name",
            name= "Garage Layer Name",
            datatype= "GPStirng",
            parameterType= "Required",
            direction= "Input"
        )
        param4 = arcpy.Parameter(
            displayName= "Campus GDB",
            name= "Campus GDB",
            datatype= "DEType",
            parameterType= "Required",
            direction= "Input"
        )
        param5 = arcpy.Parameter(
            displayName= "Buffer Distance",
            name= "Buffer Distance",
            datatype= "GPDouble",
            parameterType= "Required",
            direction= "Input"
        )

        params = [param0, param1, param2, param3, param4, param5]
        return params
```

- The rest of these parameters are the rest of the default script created by ArcPro and we do not need to edit these at this time

```python
    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
```

-  Here is where our tool starts to run once all inputs have been made **correctly** by the user. Due to the data types we have set (**Folder**, **String**, **Double**), the user will have to input the right datatype.

```python
    def execute(self, parameters, messages):
        """The source code of the tool."""
        folder_path = parameters[0].valueasText
        gdb_name = parameters[1].valueasText
        gdb_path = folder_path + '\\' + gdb_name
        arcpy.CreateFileGDB_management(folder_path, gdb_name)
    

        csv_path = parameters[2].valueasText
        garage_layer_name = parameters[3].valueasText
        garages = arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', garage_layer_name)


        input_layer = garages
        arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
        garage_points = gdb_path + '\\' + garage_layer_name

       
        campus = parameters[4].valueasText
        buildings_campus = campus + '\Structures'
        buildings = gdb_path + '\\' + 'Buildings'


        arcpy.Copy_management(buildings_campus, buildings)

        # Reporject our Garage Points
        spatial_ref = arcpy.Describe(buildings).spatialReference
        arcpy.Project_management(garage_points, gdb_path + '\Garage_Points_Reprojected', spatial_ref)

        
        buffer_distance = int(parameters[5].value)
        garageBuffer = arcpy.Buffer_analysis(gdb_path + '\Garage_Points_Reprojected', gdb_path + '\Garage_Points_Buffer', 150)
```

- Here is where we will then end our analysis by running an **intersect** on the buildings intersecting our **buffer**. One we do this, we then will want a csv showing which buildings intersect within our given distance. Once this is done, we are finished!

```python
        # Intersect our Garage Buffer with Campus Buildings
        arcpy.Intersect_analysis([garageBuffer, buildings], gdb_path + '\Garage_Building_Intersect', 'ALL')

        # New table now in our working folder
        arcpy.TableToTable_conversion(gdb_path + '\Garage_Building_Intersect.dbf', folder_path, 'BuildingsCloseBy.csv')

        return None
```


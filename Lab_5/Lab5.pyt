# -*- coding: utf-8 -*-

import arcpy


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Lab5 - Creating a Toolbox"
        self.description = ""

    def getParameterInfo(self):
        """Define the tool parameters."""
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
            datatype= "GPString",
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
            datatype= "GPString",
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
        

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

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


        spatial_ref = arcpy.Describe(buildings).spatialReference
        arcpy.Project_management(garage_points, gdb_path + '\Garage_Points_Reprojected', spatial_ref)


        buffer_distance = int(parameters[5].value)
        garageBuffer = arcpy.Buffer_analysis(gdb_path + '\Garage_Points_Reprojected', gdb_path + '\Garage_Points_Buffer', 150)


        arcpy.Intersect_analysis([garageBuffer, buildings], gdb_path + '\Garage_Building_Intersect', 'ALL')


        arcpy.TableToTable_conversion(gdb_path + '\Garage_Building_Intersect.dbf', folder_path, 'BuildingsCloseBy.csv')

        return None

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return

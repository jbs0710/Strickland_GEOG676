# -*- coding: utf-8 -*-

import arcpy
import time


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [GraduatedColorsRenderer]

class GraduatedColorsRenderer(object):                                                     
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Lab 6 - Map Generation"
        self.description = "Create Graduated Color Map of Parking Garages"
        self.canRunInBackground = False
        self.category = "Map Tools"

    def getParameterInfo(self):
        """Define parameter definitions"""
        # Here is where the user will put their Map File (Lab6)
        param0 = arcpy.Parameter(
            displayName= "Input ArcPro Project Name",
            name= "aprxInputName",
            datatype= "DEFile",
            parameterType= "Required",
            direction= "Input"
        )
        # Here is where the user will put the Map Layer to Classify (in our case, its the Garage Parking Layer)
        param1 = arcpy.Parameter(
            displayName= "Layer to Classify",
            name= "LayerToClassify",
            datatype= "GPLayer",
            parameterType= "Required",
            direction= "Input"
        )
        # Here is where the users Output Location will be (in our case, its out Lab 6 Folder)
        param2 = arcpy.Parameter(
            displayName= "Output Location",
            name= "OutputLocation",
            datatype= "DEFolder",
            direction= "Input"
        )
        # Here is where the user will create a new (copy) of our current project.
        param3 = arcpy.Parameter(
            displayName= "Output Project Name",
            name= "OutPutProjectName",
            datatype= "GPString",
            parameterType= "Required",
            direction= "Input"
        )

        params = [param0, param1, param2, param3]
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

        # When our user hits Run, our user will see a Progressor that will let them know each step of the process of our tool
        # As we will see below, our Progressor will show different messages as "time" goes and our tool (script) reaches each line and executes its objective
        readTime = 3
        start = 0
        max = 100
        step = 33

        arcpy.SetProgressor("step", "Validating Project File...", start, max, step)
        time.sleep(readTime)

        # A message the user will see under the progessor bar
        arcpy.AddMessage("Vaildating Project File...")

        # ArcPro Project Name Input
        project = arcpy.mp.ArcGISProject(parameters[0].valueAsText)

        campus = project.listMaps('Map')[0]

        # Message the user will see above the progressor bar
        arcpy.SetProgressorPosition(start + step)
        arcpy.SetProgressorLabel("Finding your Map Layer...")
        time.sleep(readTime)

        for layer in campus.listLayers():
        # Check if layer is a feature layer
            if layer.isFeatureLayer:
                # Obtain a copy of the layer's symbology
                symbology = layer.symbology
                    # Check if it has a 'renderer' attribute
                if hasattr(symbology, 'renderer'):
                    # Check if the layer's name is Layer to Classify (GarageParking)
                    if layer.name == parameters[1].valueAsText:
                        
                        # Message user will see above the progressor bar
                        arcpy.SetProgressorPosition(start + step)
                        arcpy.SetProgressorLabel("Calculating and Classifying...")

                        symbology.updateRenderer('GraduatedColorsRenderer')
                        
                        # Field used to render for our color ramp
                        symbology.renderer.classificationField = "Shape_Area"

                        # Message user will see above the progressor bar
                        arcpy.SetProgressorPosition(start + step*2)
                        arcpy.SetProgressorLabel("Cleaning Up...")

                        # Our chosen number of breaks we will have in our Color Ramp
                        symbology.renderer.breakCount = 5

                        # Color chosen within our ramp
                        symbology.renderer.colorRamp =  project.listColorRamps('Oranges (5 Classes)')[0]

                        layer.symbology = symbology
                        
                        # Message user will see below the progressor bar
                        arcpy.AddMessage("Finish Generating Layer...")
                    
                    else:
                        # This is one of the most important messages of our tool in that it will inform our user if the layer is not within our ArcPro Project
                        # If this message prints, in indicates that the user needs to move that specific layer into the ArcPro Project file
                        print("Layers NOT Found")

        # Final progessor message to the user
        arcpy.SetProgressorPosition(start + step*3)
        arcpy.SetProgressorLabel("Saving...")
        time.sleep(readTime)

        # A final message to our user, again not associated with our progressor
        arcpy.AddMessage("Saving...")

        # This will be the new (copy) ArcPro Project with our Graduated Colors Renderer layer
        project.saveACopy(parameters[2].valueAsText + "\\" + parameters[3].valueAsText + ".aprx")
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return

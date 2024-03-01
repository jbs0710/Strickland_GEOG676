# GIS Programming 
# GEOG 676
# Lab 6

# Map Generation Toolbox

- In this lab, we are creating a **toolbox**, just like we did in Lab 5. However, the difference will be in that we will generate a **Color Ramp** map, featuring our Parking Garages layer. As our tool runs, we will add **progressors** that will help our user how our tool is running in real time, showing **labeled messages** to our user of what our tool is performing, and how much time is left before our tool is finished running.

- Just like in Lab 5, we will be doing the same things to start this lab. 

    - When we open ArcPro, we will navigate to our **ArcCatalog** tab on the right hand side and right-click **Toolboxes** and select **New Python Tool**. We will name the tool and save it into our working folder. Once this is done, we refresh that same **Toolboxes** tab, refresh it, and we now see our newly created toolbox. 

    - When we click the arrow down, we see a script automatically created by Arc. We right click and edit, and we now see this default script ready for us to edit.

- In order to help our user see real time progression of our tool, we will **import time** within our tool

```python
-*- coding: utf-8 -*-

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

```
- Just like in Lab 5, this area, **getParameters** is our main area of focus as we input our edits to this script. Our user will input their **Map File**, **Layer** (in this case, **Parking Garages**), their **Output Location**, and the name of their new (copied) map, **Project Name**.

```python
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
```

- We will not be editing the rest of the remaining parameters at this time.

```python
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
```

- Here is where our tool starts to run.

- Once we hit "Run", our user will see a **progressor** pop up. This will show our user different labels and messages showing the progression of the tool, as each line is read in our code. 

```python
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

        # This is looking for our first map within our indicated folder file
        campus = project.listMaps('Map')[0]

        # Message the user will see above the progressor bar
        arcpy.SetProgressorPosition(start + step)
        arcpy.SetProgressorLabel("Finding your Map Layer...")
        time.sleep(readTime)
```

- In this portion of code, our code is looking for our layer within our map file. Our code is running an **IF/ELSE statement** making sure our layer is a correct input by our user.

- 
```python
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
                        
                        # Field used to render for our color ramp, we are telling arcpy that we want to use the "Shape_Area" field
                        symbology.renderer.classificationField = "Shape_Area"

                        # Message user will see above the progressor bar
                        arcpy.SetProgressorPosition(start + step*2)
                        arcpy.SetProgressorLabel("Cleaning Up...")

                        # Our chosen number of breaks, or how many classes we will have, in our Color Ramp
                        symbology.renderer.breakCount = 5

                        # Color chosen within our ramp
                        symbology.renderer.colorRamp =  project.listColorRamps('Oranges (5 Classes)')[0]
                        
                        # A very important step in that is sets the actual symbology equal to the copies
                        layer.symbology = symbology
                        
                        # Message user will see below the progressor bar
                        arcpy.AddMessage("Finish Generating Layer...")
                    
                    else:
                        # This is one of the most important messages of our tool in that it will inform our user if the layer is not within our ArcPro Project
                        # If this message prints, in indicates that the user needs to move that specific layer into the ArcPro Project file
                        print("Layers NOT Found")
```
- Our last few **labels and messages** to our user shows the saving of their work and the finishing touches of our tool. 

- The last portion of our tools saves out a copy of the project, now showing the actually **Graduated Color Renderer** of the **Garage Parking** layer. It is saved with the name provided by the user and in the folder location provided by the user.

```python
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
```
- One of the important lessons here is that our code has notes for the creator to keep track internally but the notes for the user are really important to have a user-friendly interaction. These **labels** and **messages** will also show what has been successful or what has failed, beginning to end.

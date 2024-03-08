# GIS Programming 
# GEOG 676
# Lab 7

# Raster Analysis

- In this lab, we are working with **raster datasets**. We will be combining TIFF files to create a **Composite** as well as using 3D analysis tools to show **Hillshade** and **Slope** using our raster dataset.

- It is very common to perform or convert from a raster to something else using ArcGIS and we will perform some basic conversions in this Lab.


- The first step in the is lab is to find our data. We will create an account on the **USGS website** to download some raster datasets. Once we have created an account and log in, we will find our **DEM** dataset and our **Landsat** dataset. USGS will give multiple options for our location we want (in this case, College Station, TX). We should pick one that looks the best.

- Once our data is downloaded, we need to save the datasets into our designated folder.

- Now we can move on to our code.

- Our **TIFF** download has multiple bands but we are wanting the 4 bands **(Blue, Green, Red, and Near Infrared)** to then combine into one **composite** output.

```python
import arcpy

# Assign Bands
source = r"M:\Staff Folders\Ben Strickland\TAMU\ArcProPython\Module8\Lab7\RasterDatasetsToUse"
# .sa stands for Spatial Analysis Module
band1 = arcpy.sa.Raster(source + r"\band1.tif") # Blue
band2 = arcpy.sa.Raster(source + r"\band2.tif") # Green
band3 = arcpy.sa.Raster(source + r"\band3.tif") # Red
band4 = arcpy.sa.Raster(source + r"\band4.tif") # NIR (Near Infrared)

combined = arcpy.CompositeBands_management([band1, band2, band3, band4], source + r"\Output_Combined.tif")

print("Finished with Combined TIFF")
```

- Our next task is to use our **3D Analysis** tool to perform a **Hillshade**. We will use our **DEM** dataset.

```python

# Hillshade
azimuth = 315
altitude = 45
shadows = "NO_SHADOWS"
z_factor = 1
# .ddd stands for "3D Analysis"
arcpy.ddd.HillShade(source + r"\DEM.tif", source + r"\Output_Hillshade.tif", azimuth, altitude, shadows, z_factor)

print("Finished with Hillshade")

```

- Our last task is to again use our **3D Analysis** tool to perform a **Slope**. We will also use our same **DEM** dataset.

```python
# Slope
output_management = "DEGREE"
z_factor = 1
# .ddd stands for "3D Analysis"
arcpy.ddd.Slope(source + r"\DEM.tif", source + r"\Output_Slope.tif", output_management, z_factor)

print("Finished with Slope")

```

- Once this has completed, we will now have 3 new **Output** datasets in our folder to view in ArcGIS Pro.
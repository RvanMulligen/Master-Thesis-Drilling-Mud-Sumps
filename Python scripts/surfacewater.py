# -*- coding: utf-8 -*-
"""
Created on Wed May 10 15:01:54 2023

@author: R. van Mulligen
"""
"""In this code, the data of each drilling mud sump is extracted from the Occurrence map of the Global
    water surface database."""
    
#%%
"""First, the used packages are imported and a code is run to ignore all upcoming warnings"""

import os
import xarray as xr 
import numpy as np
import geopandas as gpd 
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

#%%
"""In this part, the working directory is set using the location of this file
     and a shurtcut for the input and output folder is created."""
     
wd = os.path.dirname(os.path.realpath(__file__))
input_folder = os.path.join(wd, "input") 
output_folder = os.path.join(wd, "output")
#%%
"""In this section, the shapefile with the drilling mud sumps is imported using geopandas 
    and the coordinates of them is extracted"""
    
points = gpd.read_file(os.path.join(input_folder, "selected_and_sumpsflyover.shp"))
lat1 = list(points["Latitude"])
lon1 = list(points["Longitude"])

#%%
"""In this section, the occurrence map is imported using xarray"""

ds1 = xr.open_dataset(os.path.join(input_folder, "occurrence_140W_70Nv1_4_2021.tif"))

print(ds1)
#%%
"""In this section a function is created to transform coordinates of the drilling mud sumps into indices, so it can
be used for extraction in the map arrays. To used this, the minumum value of the longitude (closest to 0) and the
maximum value of the latitude of the map used is needed (In this case, the upper right corner of the map. However, in 
other cases it has to be the upper left corner.) . Also, the x and y resolution of the map is needed. 
It is created using answer of user2856 on the follwing site: 
https://gis.stackexchange.com/questions/76781/finding-index-location-of-lat-lon-point-on-raster-grid-using-arcpy """

def map_to_pixel(dataset, pointx, pointy):
    xmin = -130  #the minimum longitude of the map
    ymax = 70 #the maximum latitude of the map
    cellx = celly = 0.00025 #resolution in degrees
    x = []
    y =[]
    for i in pointx: #transforming the longitude to collumn indices
        col = int((i - xmin) / cellx)
        x.append(col)
    for j in pointy: #transfroming latitudes to row indices
        row = int((j - ymax) / -celly)
        y.append(row)
    return x, y
#%%
"""In this section, function is set for exracting the data of the drilling mud sumps using the indices created
in the previous section. First, the indices are created by calling the map_to_pixel function, then the values
are called from the map and next the values of the coordinates are extracted and put into an array with the coordinates.
At last, the array is reshaped to an array containing only the values."""

def water(dataset, pointx, pointy):
    x2, y2 = map_to_pixel(dataset, pointx, pointy)
    ds = dataset["band_data"].values
    waters = np.array(ds[:,y2, x2])
    waters = np.reshape(waters,[57,1])
    return waters 
#%%
"""In this section, a function is defined for calling the previous defination (water) to extract the data. Afterwards the
extracted data is added to to geodataframe of the drilling mud sumps."""

def data_water(df1, pointx, pointy):
    occ = water(df1, pointx, pointy)
    points["Occurence"] = occ
    
#%%
"""In this section, the function defined in the previous section (data_water) is called. The geodataframe with the 
extracted data is changed into a dataframe in preperation for export to a csv file and then it is exported to the 
output folder as a csv file."""

data_water(ds1, lon1, lat1)
points_df = pd.DataFrame(points.assign(geometry=points["geometry"].apply(lambda p: p.wkt)))
points_df.to_csv(os.path.join(output_folder, "Water data extended.csv"))








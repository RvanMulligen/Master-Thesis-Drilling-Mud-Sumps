# -*- coding: utf-8 -*-
"""
Created on Wed May 24 14:00:08 2023

@author: R van Mulligen

In this script the pH and nitrogem data of each drilling mud sump is extracted from the SoilGrids pH and nitrogen maps.
Note: a value of 0.0 means no data.
"""

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
"""In this section, the shapefile with the drilling mud sumps is imported using geopandas and lists 
of the latitudes and longitudes of the drilling mud sumps is created in preparion for the
data extraction"""

points = gpd.read_file(os.path.join(input_folder, "selected_and_sumpsflyover.shp"))
lat1 = list(points["Latitude"]) #extracting the latitudes from the drilling mud sumps geodataframe
lon1 = list(points["Longitude"]) #extracting the latitudes from the drilling mud sumps geodataframe

#%%
"""In this section, the pH and nirogen maps of different depths are imported using xarray"""

ds1 = xr.open_dataset(os.path.join(input_folder, "pH_0-5_mean.tif"))
ds2 = xr.open_dataset(os.path.join(input_folder, "pH_5-15_mean.tif"))
ds3 = xr.open_dataset(os.path.join(input_folder, "pH_15-30_mean.tif"))
ds4 = xr.open_dataset(os.path.join(input_folder, "pH_30-60_mean.tif"))
ds5 = xr.open_dataset(os.path.join(input_folder, "pH_60-100_mean.tif"))
ds6 = xr.open_dataset(os.path.join(input_folder, "pH_100-200_mean.tif"))

ds7 = xr.open_dataset(os.path.join(input_folder, "N_0-5_mean.tif"))
ds8 = xr.open_dataset(os.path.join(input_folder, "N_5-15_mean.tif"))
ds9 = xr.open_dataset(os.path.join(input_folder, "N_15-30_mean.tif"))
ds10 = xr.open_dataset(os.path.join(input_folder, "N_30-60_mean.tif"))
ds11= xr.open_dataset(os.path.join(input_folder, "N_60-100_mean.tif"))
ds12 = xr.open_dataset(os.path.join(input_folder, "N_100-200_mean.tif"))

#print(ds4)
#%%
"""In this section a function is defined to transform coordinates of the drilling mud sumps into indices, so it can
be used for extraction in the map arrays. To used this, the minumum value of the longitude  and the
maximum value of the latitude of the map used is needed (In this case, the upper right corner of the map. However, in 
other cases it has to be the upper left corner.) . Also, the x and y resolution of the map is needed. 
It is created using answer of user2856 on the follwing site: 
https://gis.stackexchange.com/questions/76781/finding-index-location-of-lat-lon-point-on-raster-grid-using-arcpy """

def map_to_pixel(dataset, pointx, pointy):
    xmin = -137  #minimum longitude of the map
    ymax = 70 #the maximum latitude of the map
    cellx = 0.002259887005649701113 #longitudal resolution in degreed
    celly = 0.002389486260454001375 #latitudal resolution in degrees
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
"""In this section, function is defined for exracting the data of the drilling mud sumps using the indices created
in the previous section. First, the indices are created by calling the map_to_pixel function, then the values
are called from the map and next the values of the coordinates are extracted and put into an array with the coordinates.
At last, the array is reshaped to an array containing only the values."""

def soil(dataset, pointx, pointy):
    x2, y2 = map_to_pixel(dataset, pointx, pointy) #calling the funcion made in the previous section for the indices
    ds = dataset["band_data"].values #getting the values from the map
    waters = np.array(ds[:,y2, x2]) #extracting the values using the indices and putting it into an array
    waters = np.reshape(waters,[57,1]) #reshaping the array to the values only
    return waters 
#%%
"""In this section, a function is defined for calling the previous function (soil) multiple times, using different 
pH maps of different depths to extract the data. Afterwards the extracted data is added to to geodataframe of 
the drilling mud sumps."""

def ph(df1, df2, df3, df4, df5,df6, pointx, pointy):
    ph0_5 = soil(df1, pointx, pointy)
    ph5_15 = soil(df2, pointx, pointy)
    ph15_30 = soil(df3, pointx, pointy)
    ph30_60 = soil(df4, pointx, pointy)
    ph60_100 = soil(df5, pointx, pointy)
    ph100_200 = soil(df6, pointx, pointy)
    points["pH 0-5cm "] = ph0_5
    points["pH 5-15cm "] = ph5_15
    points["pH 15-30"] = ph15_30
    points["pH 30-60"] = ph30_60
    points["pH 60-100"] = ph60_100
    points["pH 100-200"] = ph100_200

#%%
"""In this section, a function is defined for calling a previous function (soil) multiple times, using different
nitrogen maps of different depths. Afterwards the extracted data is added to the geodataframe of the drilling mud sumps."""

def nitrogen(df1, df2, df3, df4, df5,df6, pointx, pointy):
    n0_5 = soil(df1, pointx, pointy)
    n5_15 = soil(df2, pointx, pointy)
    n15_30 = soil(df3, pointx, pointy)
    n30_60 = soil(df4, pointx, pointy)
    n60_100 = soil(df5, pointx, pointy)
    n100_200 = soil(df6, pointx, pointy)
    points["N 0-5cm "] = n0_5
    points["N 5-15cm "] = n5_15
    points["N 15-30"] = n15_30
    points["N 30-60"] = n30_60
    points["N 60-100"] = n60_100
    points["N 100-200"] = n100_200
    
#%%
"""In this section, the functions defined in the previous sections (ph and nitrogen) are called to extract the data 
and add it to the geodataframe. The geodataframe with the extracted data is changed into a dataframe in preperation
for export to a csv file and then it is exported to the output folder as a csv file."""

ph(ds1, ds2, ds3, ds4, ds5, ds6, lon1, lat1)
nitrogen(ds7, ds8, ds9, ds10, ds11, ds12, lon1, lat1)
points_df = pd.DataFrame(points.assign(geometry=points["geometry"].apply(lambda p: p.wkt)))
points_df.to_csv(os.path.join(output_folder, "pH and N data.csv"))




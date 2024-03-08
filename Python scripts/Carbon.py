# -*- coding: utf-8 -*-
"""
Created on Wed May  3 20:21:37 2023

@author: R van Mulligen

In this script the SOC data of each drilling mud sump is extracted from the NCSCDv2 SOC maps.
Note: a value of 65535 means no data. 
"""

#%%
"""First, the used packages are imported and a code is run to ignore all upcoming warnings"""

import os
import netCDF4 as nc
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
lon1 = list(points["Longitude"]) #extracting the longitudes from the drilling mud sumps geodataframe

#%%
"""In this section, the SOC maps of different depths are imported using netCDF4."""

df1 = nc.Dataset(os.path.join(input_folder, "NCSCDv2_Canada_WGS84_SOCC30_0012deg.nc"))
df2 = nc.Dataset(os.path.join(input_folder, "NCSCDv2_Canada_WGS84_SOCC100_0012deg.nc"))
df3 = nc.Dataset(os.path.join(input_folder, "NCSCDv2_Canada_WGS84_SOCC200_0012deg.nc"))
df4 = nc.Dataset(os.path.join(input_folder, "NCSCDv2_Canada_WGS84_SOCC300_0012deg.nc"))

#%%
"""In this section, a function is defined for extracting the longitude and latitude from the SOC maps and is put
seperatly into arrays."""

def extract_lat_lon(dataset):
    lat, lon = dataset.variables['lat'], dataset.variables['lon'] #latitude and longitide is extracted from the map
    latvals = np.array(lat[:]) #the latitudes is put into an array
    lonvals = np.array(lon[:]) #the longitudes is put into an array
    return latvals, lonvals

#%%
"""In this section a function is defined for transforming coordinates of the drilling mud sumps into array indices, so it 
can be used for extraction in the map arrays. To use this, the minimum latitude and maximum longitude is needed. This is 
done by using the min and max functions of python together with the extracted coordinates of the map, done in the previous
function. Also, the x and y resolution of the map is needed. 
It is created using answer of user2856 on the follwing site: 
https://gis.stackexchange.com/questions/76781/finding-index-location-of-lat-lon-point-on-raster-grid-using-arcpy """

def map_to_pixel(dataset, pointx, pointy):
    la, lo = extract_lat_lon(dataset) #the function from the previous section is callled to give the coordinates of the map.
    xmin = lo.min()  #minimum longitude of the map
    ymax = la.max() #maximum latitude of the map
    cellx = celly = 0.012 #resolution
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
"""In this section, a function is defined for exracting the data of the drilling mud sumps using the indices created
in the previous section. First, the indices are created by calling the map_to_pixel function, then the values are 
extracted using the coordinates and put into an array with the coordinates."""

def carbon(dataset, pointx, pointy):
    x2, y2 = map_to_pixel(dataset, pointx, pointy) #calling the map_to_pixel function for the indices
    scarbon = np.array(dataset.variables["NCSCDv2"][:][y2, x2]) #extraction of the values using the coordinates
    return scarbon

#%%
"""In this section, a function is defined for calling the previous function (carbon) multiple times, using different
soc maps of different depths to extract the data. Afterwards the extracted data is added to the geodataframe of 
the drilling mud sumps."""

def soil_carbon(dataframe, ds1, ds2, ds3, ds4, pointsx, pointsy):
    sc1 = carbon(ds1, pointsx, pointsy)
    sc2 = carbon(ds2, pointsx, pointsy)
    sc3 = carbon(ds3, pointsx, pointsy)
    sc4 = carbon(ds4, pointsx, pointsy)
    dataframe["Soil Carbon 0-30cm"] = sc1
    dataframe["Soil Carbon 0-100cm"] = sc2
    dataframe["Soil Carbon 100-200cm"] = sc3
    dataframe["Soil Carbon 200-300cm"] = sc4
    return dataframe

#%%
"""In this section, the function defined in the previous section is called to extract the data and add it to the
geodataframe. The geodataframe with the extracted data is changed into a dataframe in preperation for export to a csv 
file and then it is exported to the output folder as a csv file."""
    
soilcarbon = soil_carbon(points, df1, df2, df3, df4, lon1, lat1)
points_df = pd.DataFrame(soilcarbon.assign(geometry=soilcarbon["geometry"].apply(lambda p: p.wkt)))
points_df.to_csv(os.path.join(output_folder, "Carbon data.csv"))
   




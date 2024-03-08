# -*- coding: utf-8 -*-
"""
Created on Wed May 24 11:40:59 2023

@author: R van Mulligen

In this script the soilgrids pH and nitrogen maps are downloaded via WebCoverageService (wsc).
This script is created from: 
    https://git.wur.nl/isric/soilgrids/soilgrids.notebooks/-/blob/master/02-WCS-getExtent.ipynb
    https://git.wur.nl/isric/soilgrids/soilgrids.notebooks/-/blob/master/01-WCS-basics.ipynb?ref_type=heads
If more information is needed, click on the site as it explains clearly on how to use the wcs to download
the soilgrid maps.
The script was runs twice, first for the pH variable and next for the nitrogen variable. This script shows the pH
variable, and when used for the nitrogen variable or other variable, change the names of the pH to the correct variable.
To see which name is used for each variable, check to properties table under the question "What does the file names mean?"
in the FAQ of soilgrids (https://www.isric.org/explore/soilgrids/faq-soilgrids) to see which name is used.
"""

#%%
"Here the packages are imported. Install the packages that you do not have yet using your own method."

import os
from owslib.wcs import WebCoverageService
#%%
"""First, a working directory is set using the location of this script and an shortcut to the input folder is created,
    as the maps will be stored in the input folder for following scripts where the data gets extracted."""
    
wd = os.path.dirname(os.path.realpath(__file__))
input_folder = os.path.join(wd, "input")
#%%
"""Next, the wcs is set for the correct variable. This variable is put in the end, as .../map/"put here the variable".map
In this case, the phh2o (the name for the pH map) is put as the variable and below (behind the #) is the nitrogen example"""
                                                                                    
wcs = WebCoverageService('http://maps.isric.org/mapserv?map=/map/phh2o.map',
                         version='1.0.0')
#wcs = WebCoverageService('http://maps.isric.org/mapserv?map=/map/nitrogen.map',
#                         version='1.0.0')
#%%
"""To see if the wcs correctly set, a list of the contents is printed. This content are the different maps that are 
    available for the variable that is put in."""
    
print(list(wcs.contents))

#%%
"""In the following section, the map segements of the variable within the bounding box is fetched. For this you need
the identiefier of the map, which  is gotten from the content list printed earlier. Next is the crs is set, which is in
this case EPSG 4326. Then, the bounding box is set using the coordinates of your choosing. In this case, the coordinates of the 
Mackenzie delta is used, with all the drilling mud sumps used in this study. Then, the resolution of x and y is set 
accordingly to the set crs, which means in this case it is in degrees. And last the output format of the file is set."""

response = wcs.getCoverage(
    identifier='phh2o_0-5cm_mean', 
    crs='urn:ogc:def:crs:EPSG::4326',
    bbox=(-137, 68, -132, 70), 
    resx=0.002259887005649701113, resy=0.002389486260454001375, 
    format='GEOTIFF_INT16')

response1 = wcs.getCoverage(
    identifier='phh2o_5-15cm_mean', 
    crs='urn:ogc:def:crs:EPSG::4326',
    bbox=(-137, 68, -132, 70), 
    resx=0.002259887005649701113, resy=0.002389486260454001375, 
    format='GEOTIFF_INT16')

response2 = wcs.getCoverage(
    identifier='phh2o_15-30cm_mean', 
    crs='urn:ogc:def:crs:EPSG::4326',
    bbox=(-137, 68, -132, 70), 
    resx=0.002259887005649701113, resy=0.002389486260454001375, 
    format='GEOTIFF_INT16')

response3 = wcs.getCoverage(
    identifier='phh2o_30-60cm_mean', 
    crs='urn:ogc:def:crs:EPSG::4326',
    bbox=(-137, 68, -132, 70), 
    resx=0.002259887005649701113, resy=0.002389486260454001375, 
    format='GEOTIFF_INT16')

response4 = wcs.getCoverage(
    identifier='phh2o_60-100cm_mean', 
    crs='urn:ogc:def:crs:EPSG::4326',
    bbox=(-137, 68, -132, 70), 
    resx=0.002259887005649701113, resy=0.002389486260454001375, 
    format='GEOTIFF_INT16')

response5 = wcs.getCoverage(
    identifier='phh2o_100-200cm_mean', 
    crs='urn:ogc:def:crs:EPSG::4326',
    bbox=(-137, 68, -132, 70), 
    resx=0.002259887005649701113, resy=0.002389486260454001375, 
    format='GEOTIFF_INT16')
#%%
"""Now, the coverage is fetched and saved on the set loaction on the disk. Don't forget to give each file a
    name."""
    
with open(os.path.join(input_folder, 'pH_0-5_mean.tif'), 'wb') as file:
    file.write(response.read())

with open(os.path.join(input_folder, 'pH_5-15_mean.tif'), 'wb') as file:
    file.write(response1.read())

with open(os.path.join(input_folder, 'pH_15-30_mean.tif'), 'wb') as file:
    file.write(response2.read())

with open(os.path.join(input_folder, 'pH_30-60_mean.tif'), 'wb') as file:
    file.write(response3.read())

with open(os.path.join(input_folder, 'pH_60-100_mean.tif'), 'wb') as file:
    file.write(response4.read())

with open(os.path.join(input_folder, 'pH_100-200_mean.tif'), 'wb') as file:
    file.write(response5.read())
    
#%%
"""Next, a check is performed if the maps are saved correctly by opening one of the 
maps with rasterio."""

import rasterio
ph = rasterio.open(os.path.join(input_folder, 'pH_0-5_mean.tif'), driver="GTiff")

#%%
"""Then, we plot the map to see if the values are correct. The values of pH and nitrogen are given in pHx10 and
    cg/kg. If an other variable is used, check to properties table under the question "What does the file names mean?"
    in the FAQ of soilgrids (https://www.isric.org/explore/soilgrids/faq-soilgrids) for the mapped units of those variables."""
    
from rasterio import plot
plot.show(ph, title='Mean pH between 0 and 5 cm deep in the Mackenzie Delta', cmap='gist_ncar')

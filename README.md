# Master-Thesis-Drilling-Mud-Sumps
This page is created by me, Renate van Mulligen, for my Master Thesis about drilling mud sumps.
This page contains all scripts that are used in my master thesis.
As I have used two different coding types/programs, Python and Google Earth Engenine (which uses JavaScript), I have created two folders.
In these folders the scripts are placed for the respective coding type.

In the Google Earth Engine scripts folder the scripts are txt files, due to not being able to download the code from the GEE site.
The files are: Temperature_and_Precipitation.txt for the temperature and precipition from ERA5, Elevation_and_Slope.txt for the elevation and slope from ArcticDEM
and Snowfall.txt for the snowfall from ERA5-land.

In the Python scripts folder the scripts are .py or .ipynb.
The files are: surfacewater.py for the water occurence from the Global Surface Water database, soilgrids.py for downloading the SoilGrids maps, soil.py for the pH and nitrogen from SoilGrids, carbon.py for the SOC from NCSCDv2 and k-means.ipynb for the k-means clustering analysis.
    
As I had trouble with the k-means analysis using the python version (3.8.13) installed on my computer, the k-means analysis was done with Google Colab. As the script of 
the k-means analysis is created in Google Colab, i would suggest to open the script in Google Colab.

import matplotlib.pyplot as plt
import matplotlib.colors as colors
from pysheds.grid import Grid
import rasterio
from rasterio.merge import merge
from rasterio.plot import show
import glob
import gdal
import seaborn as sns
import warnings
import os
import numpy as np
from datetime import datetime
warnings.filterwarnings('ignore')
startTime = datetime.now()


# Mosaic Conditioned Rasters and assign projection

dirpath = os.path.join('..', 'data', 'conditioned', 'n25*')
out_fp = os.path.join('..', 'data', 'conditioned', 'output', 'mosaic.tif')
search_criteria = r"n*"
q = os.path.join(dirpath, search_criteria)
print(q)
dem_fps = glob.glob(q)
print(dem_fps)
src_files_to_mosaic = []
for fp in dem_fps:
    src = rasterio.open(fp)
    src_files_to_mosaic.append(src)
print(src_files_to_mosaic)
mosaic, out_trans = merge(src_files_to_mosaic)
out_meta = src.meta.copy()

proj = '﻿Proj4: +proj=longlat +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +no_defs'  # NAD 83
out_meta.update({"driver": "GTiff", "height": mosaic.shape[1], "width": mosaic.shape[2], "transform": out_trans, "crs":
                 proj})
print("Writing file...")
with rasterio.open(out_fp, "w", **out_meta) as dest:
    dest.write(mosaic)


# Re-Project Conditioned Raster to NAD 83 Albers Equal Area

print("Reprojecting raster to NAD83 Albers Equal Area...")
os.chdir("D:\GitHub\pysheds\data\conditioned\output")
os.system('gdalwarp mosaic.tif reproject.tif -t_srs "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 '
          '+x_0=0 +y_0=0 +ellps=GRS9- +towgs84=0,0,0,0,0,0,0 +units=m _no_defs"')
os.chdir("D:\GitHub\pysheds\examples")  # Change working directory back to script location


print(startTime)
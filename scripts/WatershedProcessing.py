"""
Pysheds watershed delineation method pythons script

By mdbartos and Emily Pease

Workflow:

PYTHON:
import packages
read conditioned raster
read flow direction raster
calculate flow accumulation
change directory (os.system) to desired export location
convert flow direction to ascii --> to .tif
convert flow accumulation to ascii --> to .tif

ESRI:
project rasters, create pourpoint shapefile
snap pourpoint to flow accumulation
(dont do this unless it doesnt work in the script) use Spatial Analyst --> math --> Int tool to convert float raster to int raster
run water shed with snapped pourpoint and int raster


WOW WE HAVE A WATERSHED NOW | awesome!
Convert to shapefile, calculate the area and you're good to go


"""
import glob
import gdal
import rasterio.merge as merge
import seaborn as sns
import rasterio
import warnings
import os
import rasterio
from rasterio.merge import merge
from rasterio.plot import show
import numpy as np
from rasterio.crs import CRS
from pysheds.grid import Grid
from rasterio.warp import calculate_default_transform
from datetime import datetime
warnings.filterwarnings('ignore')
startTime = datetime.now()
# os.chdir('D:\\Projects\\Watersheds\\pysheds\\08108780\\rasters')
# files = glob.glob("D:\\Projects\\Watersheds\\pysheds\\08108780\\rasters")
# files_string = " ".join(files)
# # command = "gdal_merge.py -o mosaic.tif -of gtiff " + files_string
# # os.system('gdal_merge.py -init 255 -o mosaic.tif grdn*')
# os.system("gdal_merge.py -o mosaic.tif -of gtiff " + files_string)
# exit()





# Mosaic Conditioned Rasters and assign projection

dirpath = os.path.join('pysheds', '08108780', 'mosaic')
out_fp = os.path.join('pysheds', '08108780', 'mosaic', 'mos_31_32.tif')
search_criteria = r"1mosaic*" # delete any xmls in the folder or it wont work, sorry
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
    kwargs = src.meta
    kwargs.update(
        bigtiff='YES',
        dtype=rasterio.uint16
    )
    dest.write(mosaic)


# Re-Project Conditioned Raster to NAD 83 Albers Equal Area

# print("Reprojecting raster to NAD83 Albers Equal Area...")
# os.chdir("D:\\Projects\\Watersheds\\pysheds\\08108780\\mosaic")
# os.system('gdalwarp mosaic_34.tif reproject.tif -t_srs "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 '
#           '+x_0=0 +y_0=0 +ellps=GRS9- +towgs84=0,0,0,0,0,0,0 +units=m _no_defs"')


#
grid = Grid.from_raster(os.path.join('pysheds', 'data', 'conditioned', 'original', 'n30w100_con', 'n30w100_con'), data_name='dem')
grid.read_raster(os.path.join('pysheds', 'data', 'flowdir', 'original', 'n30w100_dir_bil', 'n30w100_dir.bil'), data_name='dir')
# grid = Grid.from_raster(os.path.join('pysheds', 'data', 'conditioned', 'reproject', '30_100_con'), data_name='dem')
# grid.read_raster(os.path.join('pysheds', 'data', 'flowdir', 'reproject', '30_100_reproj'), data_name='dir')
dirmap = (64,  128,  1,   2,    4,   8,    16,  32)
grid.accumulation(data='dir', dirmap=dirmap, out_name='acc')

print("Writing flow direction raster ...")
os.chdir('D:\Projects\Watersheds\pysheds\data\processed_DEM')
grid.to_ascii('dir', file_name='dir.ascii', view=True, apply_mask=False, delimiter=' ')
os.system('gdal_translate -ot UInt32 -of "GTiff"  dir.ascii fldir.tif')
os.system('gdalwarp -t_srs "+proj=longlat +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +no_defs" -overwrite fldir.tif fldir_int.tif')


print("writing flow accumulation raster ...")
# os.chdir('D:\Projects\Watersheds\pysheds\data\processed_DEM')
grid.to_ascii('acc', file_name='acc.ascii', view=True, apply_mask=False, delimiter=' ')
os.system('gdal_translate -of "GTiff" acc.ascii acc.tif')
os.system('gdalwarp -t_srs "+proj=longlat +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +no_defs" -overwrite acc.ascii flacc.tif')


print(datetime.now() - startTime)
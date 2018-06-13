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
import skimage
warnings.filterwarnings('ignore')
startTime = datetime.now()

# # Mosaic Conditioned Rasters and assign projection
#
# dirpath = os.path.join('..', 'data', 'conditioned', 'n*')
# out_fp = os.path.join('..', 'data', 'conditioned', 'output', 'mosaic.tif')
# search_criteria = r"n*"
# q = os.path.join(dirpath, search_criteria)
# print(q)
# dem_fps = glob.glob(q)
# print(dem_fps)
# src_files_to_mosaic = []
# for fp in dem_fps:
#     src = rasterio.open(fp)
#     src_files_to_mosaic.append(src)
# print(src_files_to_mosaic)
# print("Mosaicing rasters now ...")
# mosaic, out_trans = merge(src_files_to_mosaic)
# out_meta = src.meta.copy()
# print("Assigning projection...")
# proj = '﻿Proj4: +proj=longlat +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +no_defs'  # NAD 83
# out_meta.update({"driver": "GTiff", "height": mosaic.shape[1], "width": mosaic.shape[2], "transform": out_trans, "crs":
#                  proj})
# print("Writing file...")
# with rasterio.open(out_fp, "w", **out_meta) as dest:
#     dest.write(mosaic)
#
#
# # Re-Project Conditioned Raster to NAD 83 Albers Equal Area
#
# print("Reprojecting raster to NAD83 Albers Equal Area...")
# os.chdir("D:\GitHub\pysheds\data\conditioned\output")
# os.system('gdalwarp mosaic.tif reproject.tif -t_srs "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 '
#           '+x_0=0 +y_0=0 +ellps=GRS9- +towgs84=0,0,0,0,0,0,0 +units=m _no_defs"')
# os.chdir("D:\GitHub\pysheds\examples")  # Change working directory back to script location


# Read in Conditioned (mosaiced + reprojected) raster
print("Reading grid of conditioned raster ...")

grid = Grid.from_raster(os.path.join('..', 'data', 'raster', 'grdn31w098_13'), data_name='dem')

fig, ax = plt.subplots(figsize=(8, 6))
fig.patch.set_alpha(0)
plt.imshow(grid.dem, vmin=0, vmax=3000, extent=grid.extent, cmap='cubehelix', zorder=1)
plt.colorbar(label='Elevation (m)')
plt.grid(zorder=0)
plt.title('Digital elevation map')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
# plt.savefig('img/conditioned.png', bbox_inches='tight')


# print("Reading in Flow Direction raster ...")
# grid.read_raster(os.path.join('..', 'data', 'flowdir', 'n30w095_dir_bil', 'n30w095_dir.bil'), data_name='dir')
print("calculating flow direction now ...")
grid.flowdir(data='dem', dirmap=(64, 128, 1, 2, 4, 8, 16, 32))
print(grid.dir)
print(grid.dir.size)
print("assigning direction of flow (N, NE, SE, etc) ...")
dirmap = (64, 128, 1, 2, 4, 8, 16, 32) # Specify flow direction values (N    NE    E    SE    S    SW    W    NW)


print('calculating flow accumulation ...')
# grid.accumulation(data='catch', dirmap=dirmap, out_name='acc')
grid.accumulation(data='dir', dirmap=dirmap, out_name='acc')
print('plotted flow accumulation ...')
fig, ax = plt.subplots(figsize=(8, 6))
fig.patch.set_alpha(0)
plt.grid('on', zorder=0)
acc_img = np.where(grid.mask, grid.acc + 1, np.nan)
im = ax.imshow(acc_img, extent=grid.extent, zorder=2,
               cmap='cubehelix',
               norm=colors.LogNorm(1, grid.acc.max()))
plt.title('Flow Accumulation')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
# plt.savefig('img/flow_accumulation.png', bbox_inches='tight')

plt.show()

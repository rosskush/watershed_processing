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


# # Mosaic Conditioned Rasters and assign projection
#
# dirpath = os.path.join('..', 'data', 'conditioned', 'n25*')
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
# mosaic, out_trans = merge(src_files_to_mosaic)
# out_meta = src.meta.copy()
#
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
#

# Read in Conditioned (mosaiced + reprojected) raster
print("Reading grid of conditioned raster ...")
grid = Grid.from_raster(os.path.join('..', 'data', 'conditioned', 'n25w100_con', 'n25w100_con'), data_name='dem')
# grid = Grid.from_raster(os.path.join('..', 'data', 'conditioned', 'output', 'reproject.tif'), data_name='dem')
# grid = Grid.from_raster(os.path.join('..', 'data', 'conditioned', 'n30w095_con', 'n30w095_con'), data_name='dem')
# grid = Grid.from_raster(os.path.join('..', 'data', 'conditioned', 'n30w100_con', 'n30w100_con'), data_name='dem')
fig, ax = plt.subplots(figsize=(8, 6))
fig.patch.set_alpha(0)
plt.imshow(grid.dem, vmin=0, vmax=3000, extent=grid.extent, cmap='cubehelix', zorder=1)
plt.colorbar(label='Elevation (m)')
plt.grid(zorder=0)
plt.title('Digital elevation map')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.savefig('img/conditioned.png', bbox_inches='tight')


# # Mosaic flow direction raster and assign projection
#
# dirpath = os.path.join('..', 'data', 'flowdir', 'n25*')
# out_fp = os.path.join('..', 'data', 'flowdir', 'output', 'flowdir_mosaic.tif')
# search_criteria = r"*.bil"
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
# # Reproject flow direction rasters to NAD 83 Albers Equal Area
#
# print("Reprojecting Flow Direction raster to NAD83 Albers Equal Area...")
# os.chdir("D:\\GitHub\\pysheds\\data\\flowdir\\output")
# os.system('gdalwarp flowdir_mosaic.tif reproject_fldir.tif -t_srs "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 '
#           '+x_0=0 +y_0=0 +ellps=GRS9- +towgs84=0,0,0,0,0,0,0 +units=m _no_defs"')
# os.chdir("D:\GitHub\pysheds\examples")  # Change working directory back to script location

# Flow direction

print("Reading in Flow Direction raster ...")
# grid.read_raster(os.path.join('..', 'data', 'flowdir', 'output', 'reproject_fldir.tif'), data_name='dir')
grid.read_raster(os.path.join('..', 'data', 'flowdir', 'n25w100_dir_bil', 'n25w100_dir.bil'), data_name='dir')
print("calculating flow direction now ...")
# grid.flowdir(data='dem', dirmap=(64, 128, 1, 2, 4, 8, 16, 32))
print(grid.dir)
print(grid.dir.size)
print("assigning direction of flow (N, NE, SE, etc) ...")
dirmap = (64, 128, 1, 2, 4, 8, 16, 32) # Specify flow direction values (N    NE    E    SE    S    SW    W    NW)

fig = plt.figure(figsize=(8, 6))
fig.patch.set_alpha(0)
plt.imshow(grid.dir, cmap='viridis', zorder=2)
boundaries = ([0] + sorted(list(dirmap)))
plt.colorbar(boundaries=boundaries, values=sorted(dirmap))
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Flow direction grid')
plt.grid(zorder=-1)
plt.tight_layout()
plt.savefig('img/flow_direction.png', bbox_inches='tight')



# Snap pour point


# x, y = -98.40260833333333, 29.235411111111112
# x, y = -97.2923, 32.7337
# x, y = -97.294167, 32.73750
# xy = [x, y]
# print(xy)
#
# # grid.nearest_cell(x, y)
#
#
# print("Snap pour point ...")
# grid.snap_to_mask(mask=grid.dir, xy=xy, return_dist=True)
#
# print("Catchment time")
# grid.catchment(data='dir', x=x, y=y, dirmap=dirmap, out_name='catch',
#                recursionlimit=15000, xytype='label', nodata_out=0)
# print('clipping area to catchment area...')
# grid.clip_to('catch')  # Clip the bounding box to the catchment
# catch = grid.view('catch', nodata=np.nan)  # Get a view of the catchment
#
# print('plotting catchment...')
# fig, ax = plt.subplots(figsize=(8,6))
# fig.patch.set_alpha(0)
# plt.grid('on', zorder=0)
# im = ax.imshow(catch, extent=grid.extent, zorder=1, cmap='viridis')
# plt.colorbar(im, ax=ax, boundaries=boundaries, values=sorted(dirmap), label='Flow Direction')
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.title('Delineated Catchment')
# plt.show()

# Flow accumulation

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
plt.savefig('img/flow_accumulation.png', bbox_inches='tight')

#
# print(' export flow direction')
os.chdir('D:\\GitHub\\pysheds\\data\\test1')
# print("to ascii")
# grid.to_ascii('dir', file_name='dir.ascii', view=True, apply_mask=False, delimiter=' ')
# print('to tif')
# os.system('gdal_translate -of AAIGrid dir.ascii fldir.bil')
# print('assign projection')
# os.system('gdalwarp -t_srs "+proj=longlat +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +no_defs" -overwrite fldir.bil fldir_proj.bil')
# print('reproject to NAD83 ...')
# os.system('gdalwarp fldir_proj.bil fldir_NAD83albers.bil -t_srs "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 '
#           '+x_0=0 +y_0=0 +ellps=GRS9- +towgs84=0,0,0,0,0,0,0 +units=m _no_defs"')

print('export flacc')
print('to ascii')
grid.to_ascii('acc', file_name='flacc.ascii', view=True, apply_mask=False, delimiter=' ')
print('to tif')
os.system('gdal_translate -of AAIGrid flacc.ascii flacc_test2.bil')
print('assign projection')
# os.system('gdalwarp -t_srs "+proj=utm +zone=14 +ellps=GRS80 +datum=NAD83 +units=m +no_defs" -overwrite flacc_test2.tif flacc_test3.tif')
os.system('gdalwarp -t_srs "+proj=longlat +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +no_defs" -overwrite flacc_test2.bil flacc_test3.bil')
print('reproject to NAD83 ...')
os.system('gdalwarp flacc_test3.bil NAD83_flacc.bil -t_srs "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 '
          '+x_0=0 +y_0=0 +ellps=GRS9- +towgs84=0,0,0,0,0,0,0 +units=m _no_defs"')

# dont touch anything - this works ......

plt.show()

exit()





branches = grid.extract_river_network('dir', 'acc', threshold=100, dirmap=dirmap)
fig, ax = plt.subplots(figsize=(6.5,6.5))

plt.grid('on', zorder=0)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('River network (>200 accumulation)')
plt.xlim(grid.bbox[0], grid.bbox[2])
plt.ylim(grid.bbox[1], grid.bbox[3])
ax.set_aspect('equal')

for branch in branches['features']:
    line = np.asarray(branch['geometry']['coordinates'])
    plt.plot(line[:, 0], line[:, 1])
plt.show()



# os.chdir('D:\\GitHub\\pysheds\\data\\test1')
# grid.to_ascii('dir', file_name='dir.ascii', view=True, apply_mask=False, delimiter=',')
# os.system('gdal_translate -of "GTiff" dir.ascii fldir.tif')
# os.system('gdalwarp -t_srs "+proj=longlat +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +no_defs" -overwrite fldir.tif fldir_proj.tif')
# os.system('gdalwarp fldir_proj.tif fldir_NAD83albers.tif -t_srs "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 '
#           '+x_0=0 +y_0=0 +ellps=GRS9- +towgs84=0,0,0,0,0,0,0 +units=m _no_defs"')
#
# grid.to_ascii('acc', file_name='flacc.ascii', view=True, apply_mask=False, delimiter=' ')
# os.system('gdal_translate -of AAIGrid flacc.ascii flacc_test2.tif')
# os.system('gdalwarp -t_srs "+proj=utm +zone=14 +ellps=GRS80 +datum=NAD83 +units=m +no_defs " -overwrite flacc_test2.tif flacc_test3.tif')
# os.system('gdalwarp flacc_test3.tif reproj_test3.tif -t_srs "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 ''+x_0=0 +y_0=0 +ellps=GRS9- +towgs84=0,0,0,0,0,0,0 +units=m _no_defs"')
print(datetime.now() - startTime)
plt.show()
exit()
# os.system('gdalwarp -t_srs "+proj=utm +zone=14 +ellps=GRS80 +datum=NAD83 +units=m +no_defs " -overwrite flaccumulation.ascii flaccumulation.tif')
# os.system('gdalwarp flaccumulation.tif reproj_flacc.tif -t_srs "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 ''+x_0=0 +y_0=0 +ellps=GRS9- +towgs84=0,0,0,0,0,0,0 +units=m _no_defs"')
#
# os.system('gdalwarp flowdir_mosaic.tif reproject_fldir.tif -t_srs "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 ''+x_0=0 +y_0=0 +ellps=GRS9- +towgs84=0,0,0,0,0,0,0 +units=m _no_defs"')
# os.system('-mo DATUM=WGS84 -mo PROJ=GEODETIC -a_ullr 7 47 8 46 test.ecw')
# grid.to_ascii(os.path.join('flacc.tif'), file_name='flacc.ascii', view=True, apply_mask=False, delimiter=' ')


# os.chdir("D:\\GitHub\\pysheds\\data\\flacc_out")
#
#
# os.system('gdalwarp acc reproject_flacc.tif -t_srs "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 '
#           '+x_0=0 +y_0=0 +ellps=GRS9- +towgs84=0,0,0,0,0,0,0 +units=m _no_defs"')
#


# Raster to shapefile

ws_poly = grid.polygonize()
fig, ax = plt.subplots(figsize=(6.5, 6.5))

for ws in ws_poly:
    coords = np.asarray(ws[0]['coordinates'][0])
    ax.plot(coords[:, 0], coords[:, 1], color='k')

ax.set_xlim(grid.bbox[0], grid.bbox[2])
ax.set_ylim(grid.bbox[1], grid.bbox[3])
ax.set_title('Catchment boundary (vector)')

import shutil
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon

print(ws)
print(type(ws))
print(ws[0])
print(ws[0]['coordinates'][0])
coords = Polygon(np.asarray(ws[0]['coordinates'][0]))
print(coords)
gps = gpd.GeoSeries(coords,crs={'init' :'epsg:4269'})
print(gps)
gps.crs = {'init':'epsg:4269'}
# gdf = gpd.GeoDataFrame(geometry=coords)
gps.to_file(os.path.join('..', 'data', 'ws_out','ws.shp'))
shutil.copy(os.path.join('..', 'data', 'ws_out', 'NAD_83.prj'), os.path.join('..', 'data', 'ws_out', 'ws.prj'))


# ws = ws.area/ 10**6
# print(ws.head(2))

print(datetime.now() - startTime)
# print(ws_poly)


plt.show()

# plt.show()















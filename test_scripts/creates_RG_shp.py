import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import os
# df = pd.read_excel('RioGrandeSites.xlsx')
# # print(df.head())
# shp = df['DEC_LONG_VA', 'DEC_LAT_VA']
# shp = gpd.GeoDataFrame(df, geometry='geometry')
# df.crs= "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs" #WGS84
# df.to_file('RGsite.shp')
masterDF = pd.read_excel('RioGrandeSites.xlsx')
masterDF['geometry'] = masterDF.apply(lambda xy: Point(xy['DEC_LONG_VA'],xy['DEC_LAT_VA']),axis=1)
masterDF = masterDF[['geometry', 'DRAIN_AREA_VA', 'CONTRIB_DRAIN_AREA_VA', 'STATION_NM', 'SITE_NO']]
# masterDF['geometry'] = masterDF['geometry'].astype(str)
# masterDF['DEC_LAT_VA'] = masterDF['DEC_LAT_VA'].astype(float)

proj4 = '+proj=longlat +ellps=GRS80 +datum=NAD83 +no_defs ' # from epsg 4269
masterDF = gpd.GeoDataFrame(masterDF,geometry='geometry' ,crs=proj4)
# print(masterDF.head())

# now reporject to nad83 albers
proj4_albers = '+proj=aea +lat_1=27.5 +lat_2=35 +lat_0=18 +lon_0=-100 +x_0=1500000 +y_0=6000000 +ellps=GRS80 +datum=NAD83 +units=m +no_defs ' # i'm guessing it is this one http://spatialreference.org/ref/epsg/3083/ but double check
masterDF.to_crs(proj4_albers)
print(masterDF.dtypes())
masterDF.to_file(os.path.join('output', 'shapefiles', 'RioGrandeSites.shp'))
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
masterDF = gpd.GeoDataFrame(masterDF,geometry='geometry') #,crs={'init':'epsg:4269'})
# print(masterDF.head())
print(masterDF.dtypes())
masterDF.to_file(os.path.join('output', 'shapefiles', 'RioGrandeSites.shp'))
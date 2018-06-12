import geopandas as gpd
import os

ws = gpd.read_file(os.path.join('ws_poly2.shp'))
print(ws.head())
ws = ws.to_crs({'init': 'epsg:3665'})

watersheds = os.path.join('shapefiles')
for water in watersheds:
    # ws['Site_ID'] = ws[]
    ws['Area_sq_mi'] = ws['geometry'].area * (3.86102e-7)  # convert sq meter to sq miles

print(ws.head())
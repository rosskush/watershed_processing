import geopandas as gpd
import os
import glob
import glob2
import simplekml

os.chdir("shp_out")
os.system("pwd")
sites = ['08108780', '0810588650']
for site in sites:
    gdf = gpd.read_file(f'ws_poly_{site}.shp')
    gdf = gdf.to_crs({'init': 'epsg:3665'})
    gdf['Area_sq_mi'] = gdf['geometry'].area * (3.86102e-7) # convert sq meter to sq miles
    gdf['Site_ID'] = site
    print(gdf.head())

    # kml = simplekml.Kml()
    # gdf.apply(lambda X: kml.newpoint(name=X['EP_{site}'], coords=[(gdf['geometry'])] ,axis=1))
    # kml.save(path = "EP_{site}.kml")






"""

This is a script to convert degree minute second to decimal degree for use in the Pysheds watershed delineation

"""


#Longitude
D_lon = 97
M_lon = 4
s_lon = 11.17

# Latitude
D_lat = 30
M_lat = 30
s_lat = 46.46

decimal_degree_lat = D_lat + (M_lat/60) + (s_lat/3600)
decimal_degree_lon = (D_lon + (M_lon/60) + (s_lon/3600)) * -1

print(str('Longitude in Decimal Degrees = ')+ str(decimal_degree_lon))
print(str('Latitude in Decimal Degrees = ')+ str(decimal_degree_lat))

### WEBMAP BASED ON FOLIUM MODULE
##### TEST1: MARKERS FOR VOLCANO LOCATIONS IMPORTED FROM CSV
##### TEST2: POLYGON BORDERS WITH COLORING BASED ON POPULATION

import folium
import csv

def popup_info(name, value):
    return '{}: {}'.format(name, value)

def elevation_color(elev):
    if elev >= 3000:
        return 'red'
    elif elev >= 2000:
        return 'orange'
    elif elev >= 1000:
        return 'lightgreen'
    else:
        return 'green'


# read from a csv file and create list with following attributes
# [0] = latitude, [1] = longitude, [2] = name, [3] = location, [4] = status, [5] = elevation
with open('resources/volcanoes.txt', newline='') as volcanoes:
    reader = csv.reader(volcanoes)
    volcanoes_lst = []
    for row in reader:
        try:
            volcanoes_lst.append([float(row[8]), float(row[9]), row[2], row[3], row[4], float(row[5])])
        except:
            continue

### create a map based on center of USA
starting_coordinates = [40.6106911, -106.4657617]
map = folium.Map(location=starting_coordinates, zoom_start=4, tiles="Stamen Terrain")


### populate child map MARKER layer of volcanoes from csv
fg_volcanoes = folium.FeatureGroup(name="Volcanoes Markers")
for coordinates in volcanoes_lst:
    # popup information
    info = '{} \n{} \n{} \n{} meters'.format(popup_info('Name', coordinates[2]),
                                             popup_info('Location', coordinates[3]),
                                             popup_info('Status', coordinates[4]),
                                             popup_info('Elevation', int(coordinates[5])))
    # pinpoint on map
    fg_volcanoes.add_child(folium.Marker(location=[coordinates[0],coordinates[1]], 
                                         popup=info, 
                                         icon=folium.Icon(color=elevation_color(coordinates[5]))))


### create child map POLYGON layer with borders and coloring based on population
polygon_data = folium.GeoJson(data=open('resources/world_borders.json', 'r', encoding='utf-8-sig').read(), 
                              style_function=lambda x: {'fillColor':'red' if x['properties']['POP2005'] > 20000000 
                                                        else 'orange' if 10000000 > x['properties']['POP2005'] 
                                                        else 'green'})

fg_world_polygons = folium.FeatureGroup(name="Population colored Polygons")
fg_world_polygons.add_child(polygon_data)


### add layers to map and save to html
map.add_child(fg_volcanoes)
map.add_child(fg_world_polygons)
map.add_child(folium.LayerControl())
map.save("map.html")

import folium
from flask import render_template
from database import get_map_daten
from folium.plugins import MiniMap


# def get_map():
#     # baslangic yeri
#     map = folium.Map(location=[51.7845, 9.3976], zoom_start=12, tiles='OpenStreetMap', width=1200, height=600)
#
#     fg = folium.FeatureGroup(name="Stations")
#
#     # Func = open("Stations.html", "a")
#
#     map_daten = get_map_daten()
#
#     for row in map_daten:
#         Stationsindex, Breite, Länge = row
#         marker = folium.Marker(location=[Breite, Länge], popup=f"Station {Stationsindex}")
#         marker.add_to(fg)
#     fg.add_to(map)
#
#     minimap = MiniMap(toggle_display=True)
#     map.add_child(minimap)
#     # Func.write("<html>\n<head>\n<title> \nOutput Data in an HTML file < / title >\n < / head > < body > < h1 > Welcometo < u > Germany < / u > < / h1 > \n < h2 > A < u > CS < / u > Portalfor Everyone< / h2 >  \n < / body > < / html > ")
#     # Func.close()
#     map.save('templates/stations.html')
#
#     return render_template('stations.html', stations=map_daten)
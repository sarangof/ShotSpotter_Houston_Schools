import geopandas as gpd
import folium
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# Load shapefile
gdf = gpd.read_file('https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Lineas_metro.geojson')
detalles = pd.read_csv('https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes_detalles.csv',sep=';')
gdf = gdf.merge(detalles, on='ESTACION', how='left')

# Dictionary mapping station names to image paths
station_to_original_image = {
    'ACEVEDO': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Originales/Acevedo.png',
    'AGUACATALA': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Originales/Aguacatala.png',
    'AYURA': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Originales/Ayura.png',
    'BELLO': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Originales/Bello.png',
    'CARIBE': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Originales/Caribe.png',
    'CISNEROS': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Originales/Cisneros.png',
    'ENVIGADO': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Originales/Envigado.png',
    'ESTADIO': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Originales/Estadio.png',
    'FLORESTA': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Originales/Floresta.png',
    'HOSPITAL': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Originales/Hospital.png',
    'INDUSTRIALES': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Originales/Industriales.png',
    'ITAGUÍ': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Originales/Itaguí.png',
    'MADERA': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Originales/Madera.png',
    'PARQUE BERRÍO': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Originales/Parque_Berrío.png',
    'POBLADO': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Originales/Poblado.png',
    'PRADO': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Originales/Prado.png',
    'SAN ANTONIO': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Originales/San_Antonio_B.png',
    'SAN JAVIER': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Originales/San_Javier.png',
    'SURAMERICANA': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Originales/Suramericana.png',
    'TRICENTENARIO': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Originales/Tricentenario.png',
    'UNIVERSIDAD': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Originales/Universidad.png'
    # Add more stations and image paths as needed
}

station_to_image = {
    'ACEVEDO': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Procesadas/Acevedo.png?raw=true',
    'AGUACATALA': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Procesadas/Aguacatala.png?raw=true',
    'AYURA': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Procesadas/Ayura.png?raw=true',
    'BELLO': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Procesadas/Bello.png',
    'CARIBE': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Procesadas/Caribe.png',
    'CISNEROS': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Procesadas/Cisneros.png',
    'ENVIGADO': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Procesadas/Envigado.png',
    'ESTADIO': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Procesadas/Estadio.png',
    'FLORESTA': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Procesadas/Floresta.png',
    'HOSPITAL': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Procesadas/Hospital.png',
    'INDUSTRIALES': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Procesadas/Industriales.png',
    'ITAGUÍ': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Procesadas/Itaguí.png',
    'MADERA': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Procesadas/Madera.png',
    'PARQUE BERRÍO': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Procesadas/Parque Berrío.png',
    'POBLADO': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Procesadas/Poblado.png',
    'PRADO': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Procesadas/Prado.png',
    'SAN ANTONIO': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Procesadas/San Antonio B.png',
    'SAN JAVIER': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Procesadas/San Javier.png',
    'SURAMERICANA': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Procesadas/Suramericana.png',
    'TRICENTENARIO': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Procesadas/Tricentenario.png',
    'UNIVERSIDAD': 'https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Virgenes/Procesadas/Universidad.png'
    # Add more stations and image paths as needed
}


icon_width = 30
def calculate_icon_height(icon_width, icon_url):
    response = requests.get(icon_url)
    # Open the image from the downloaded content
    with Image.open(BytesIO(response.content)) as img:
        # Get the width and height of the image
        width, height = img.size
        # Calculate the aspect ratio
        aspect_ratio = width / height
        icon_height = icon_width/aspect_ratio
        return icon_height

# Initialize map centered at median coordinates with a "sober" basemap
map_center = [gdf.geometry.y.median(), gdf.geometry.x.median()]
m = folium.Map(location=map_center, zoom_start=12, tiles='Stamen Terrain', attr='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, Imagery © <a href="http://stamen.com">Stamen Design</a>')

lineas_transporte = gpd.read_file('https://raw.githubusercontent.com/sarangof/Virgenes_MDE/main/Corredores_para_Transporte_de_Pasajeros/Corredores_para_Transporte_de_Pasajeros.shp')        

folium.GeoJson(
    lineas_transporte,
        style_function=lambda feature: {
        'color': 'gray',  # Line color
        'weight': 0.5  # Line width
    }
).add_to(m) 

# Add markers with custom icons and hover information
for _, row in gdf.iterrows():
    # Get station name
    station = row['ESTACION']
    # Get corresponding image path from the dictionary
    icon_url = station_to_image.get(station, None)
    original_image_path = station_to_original_image.get(station, None)
    if icon_url:
        icon_height = calculate_icon_height(icon_width,icon_url)
# Add marker with custom icon and hover information
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            #marker_size = (32,32),
            icon=folium.CustomIcon(icon_url, icon_size=(icon_width, icon_height)),
            tooltip= f'<b>{row["Nombre_estación"]}</b><br>',
            popup=f'<div style="width: 200px; padding-top:0px; padding-bottom:0px">'
                #f'<b>{row["ESTACION"]}</b><br>'
                f'<div style="text-align:center; margin-bottom:0ptx; padding-top:0px; padding-bottom:0px"><b>{row["ESTACION"]}</b></div><br>'
                f'<div style="text-align:center; padding-top:0px; ">' 
                f'<img src='+original_image_path+' alt="Image" style="width:100px;"><br>'
                f'</div>'  # Close div for centered image
                f'<div style="text-align: left; margin-bottom:0ptx; padding-top:10px; padding-bottom:0px">{row["Título"]}</div><br>'
                f'<div style="text-align: left; margin-bottom:0ptx; padding-top:0px; padding-bottom:0px"><b>Artista: </b>{row["Artista"]}, {int(row["Año"])}</div><br>'
                f'<div style="text-align: left; margin-bottom:0ptx; padding-top:0px; padding-bottom:0px"><b>Técnica: </b>{row["Técnica"]}</div><br>' 
                f'<div style="text-align: left;" white-space: nowrap; overflow: hidden; text-overflow: ellipsis;>{row["Detalles"]}</div><br>'
                f'</div>'  # Close div for tooltip 
        ).add_to(m)
    else:
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            tooltip=row['ESTACION'],  # Display station name on hover
            color='gray',  # Marker color
            fill=True,
            fill_color='gray',  # Marker fill color
            fill_opacity=0.8,  # Marker fill opacity
            radius=0.7  # Marker size
        ).add_to(m)

# Show map


m.save('virgenes_MDE.html')
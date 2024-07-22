import geopandas as gpd
import folium
from folium.plugins import BeautifyIcon

# File paths
schools_gdf = gpd.read_file('../data/schools_within_shotspotter_districts.geojson').to_crs('epsg:4269')
districts_gdf = gpd.read_file('../data/Texas_school_districts_Shotspotter.geojson')

# Create a Folium map centered around the mean location of the schools
m = folium.Map(
                location=[schools_gdf.geometry.centroid.y.mean(), schools_gdf.geometry.centroid.x.mean()], 
                zoom_start=12,
                tiles='CartoDB positron',  # Use CartoDB Positron for a simple, monochromatic base map
                attr='CartoDB Positron tiles'
                )

folium.GeoJson(
    districts_gdf,
    style_function=lambda x: {'fillColor': 'none', 'color': 'blue', 'weight': 2, 'opacity': 0.5},
    tooltip=folium.GeoJsonTooltip(fields=['NAME'], aliases=['District Name:'], localize=True)
).add_to(m)

def return_icon(row):
    if row['School_relative_to_nearest_shotspotter'] == 'All other schools':
        return BeautifyIcon(
            icon='circle',
            inner_icon_style='color:gray;font-size:5px;',
            background_color='transparent',
            border_color='transparent'
            )
    elif row['School_relative_to_nearest_shotspotter'] == '0.5 miles':
        return BeautifyIcon(
            icon='star',
            inner_icon_style='color:pink;font-size:10px;',
            background_color='transparent',
            border_color='transparent'
            )
    elif row['School_relative_to_nearest_shotspotter'] == '0.1 miles':
        return BeautifyIcon(
            icon='star',
            inner_icon_style='color:pink;font-size:10px;',
            background_color='transparent',
            border_color='transparent'
            )
    elif row['School_relative_to_nearest_shotspotter'] == 'Shotspotter':
        return BeautifyIcon(
            icon='star',
            inner_icon_style='color:red;font-size:10px;',
            background_color='transparent',
            border_color='transparent'
            )
    else:
        return 'gray'  # default color

# Add school locations to the map with different colors
for _, row in schools_gdf.iterrows():
    folium.Marker(
        location=[row.geometry.centroid.y, row.geometry.centroid.x],
        icon=return_icon(row),
        tooltip= f'<b>{row["USER_School_Name"]}</b><br>',
        popup=folium.Popup(f"{row['USER_School_Name']}<br>Percent Black: {row['percent_black']:.1f}%<br>Percent Hispanic: {row['percent_hispanic']:.1f}%", max_width=300)
        ).add_to(m)

#Add a legend to the map
legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; width: 160px; height: auto; background: white; padding: 10px; border-radius: 5px; box-shadow: 0 0 5px rgba(0,0,0,0.5); z-index:9999; id="legend"">
        <h4>Legend</h4>
        <i style="background:gray; width: 16px; height: 16px; display: inline-block; margin-right: 8px;"></i> All other schools<br>
        <i style="background:pink; width: 16px; height: 16px; display: inline-block; margin-right: 8px;"></i> 0.5 miles<br>
        <i style="background:pink; width: 16px; height: 16px; display: inline-block; margin-right: 8px;"></i> 0.1 miles<br>
        <i style="background:red; width: 16px; height: 16px; display: inline-block; margin-right: 8px;"></i> Shotspotter
    </div>
'''

# Add custom JavaScript for the legend
m.get_root().html.add_child(folium.Element(legend_html))

m.save('../school_map.html')
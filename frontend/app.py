# inside app.py
# need to upgrade shapely to 1.8.5

from greppo import app
import geopandas as gpd

app.base_layer(
    name="Open Street Map",
    visible=True,
    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    subdomains=None,
    min_zoom = 11,
    max_zoom = 12,
    attribution='(C) OpenStreetMap contributors',
)

app.base_layer(provider="CartoDB Positron")

regions = gpd.read_file("/Users/xiaohan/dsa3101-2210-13-lta/frontend/boundary.geojson")
roads = gpd.read_file("/Users/xiaohan/dsa3101-2210-13-lta/frontend/singapore_roads_cleaned_up.geojson")
cameras = gpd.read_file("/Users/xiaohan/dsa3101-2210-13-lta/frontend/singapore_camera.geojson")

app.vector_layer(
    data = regions,
    name = "Regions of Singapore",
    description = "Polygons showing the boundaries of regions of Singapore.",
    style = {"fillColor": "#4daf4a"},
)

app.vector_layer(
    data = roads,
    name = "Highways in Singapore",
    description = "Lines showing the major highways in Singapore.",
    style = {"color": "#377eb8"},
)

app.vector_layer(
    data = cameras,
    name = "Road Cameras of Singapore",
    description = "Points showing the cameras in Singapore.",
    style = {"color": "#e41a1c"},
    visible = True,
)
          
      
      


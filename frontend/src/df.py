import dash_leaflet as dl
import dash_leaflet.express as dlx
import pandas as pd
from dash_extensions.javascript import assign
from dash import Dash, html
# cd into dsa3101-2210-13-lta

colorscale = ['green','yellow', 'red']  # rainbow
chroma = "https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"  # js lib used for colors
df = pd.read_csv("/backend/model/train_data.csv") 
df = df.sort_values('traffic_density', ascending = False).drop_duplicates(subset='camera_id').sort_index()

traffic = pd.read_csv("/frontend/src/traffic_images.csv")
traffic = traffic.drop_duplicates(subset=['CameraID'])
traffic = traffic[['CameraID','Latitude','Longitude']]
df = pd.merge(traffic, df, how="left", left_on ="CameraID", right_on = "camera_id")
color_prop = 'traffic_density'
df = df[['Latitude', 'Longitude', 'CameraID', color_prop]]
dicts = df.to_dict('records')
for item in dicts:
    item["tooltip"] = 'Camera '+ "{}: Traffic Density ({:.3f})".format(item['CameraID'], item[color_prop])  # bind tooltip
geojson = dlx.dicts_to_geojson(dicts, lon="Longitude", lat="Latitude")
geobuf = dlx.geojson_to_geobuf(geojson)
vmax = df[color_prop].max()
colorbar = dl.Colorbar(colorscale=colorscale, width=20, height=150, min=0, max=vmax, unit='/lane')
# Geojson rendering logic, must be JavaScript as it is executed in clientside.
point_to_layer = assign("""function(feature, latlng, context){
    const {min, max, colorscale, circleOptions, colorProp} = context.props.hideout;
    const csc = chroma.scale(colorscale).domain([min, max]);  // chroma lib to construct colorscale
    circleOptions.fillColor = csc(feature.properties[colorProp]);  // set color based on color prop.
    return L.circleMarker(latlng, circleOptions);  // sender a simple circle marker.
}""")
# Create geojson.
geojson = dl.GeoJSON(data=geobuf, id="geojson", format="geobuf",
                     zoomToBounds=True,  # when true, zooms to bounds when data changes
                     options=dict(pointToLayer=point_to_layer),  # how to draw points
                     superClusterOptions=dict(radius=50),   # adjust cluster size
                     hideout=dict(colorProp=color_prop, circleOptions=dict(fillOpacity=1, stroke=False, radius=5),
                                  min=0, max=vmax, colorscale=colorscale))
# Create the app.
app = Dash(external_scripts=[chroma], prevent_initial_callbacks=True)
app.layout = html.Div([
    dl.Map([dl.TileLayer(), geojson, colorbar]),
], style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block", "position": "relative"})


if __name__ == '__main__':
    app.run_server(port = 8066)

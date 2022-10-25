import dash_leaflet as dl
import dash_leaflet.express as dlx
import pandas as pd
from dash_extensions.javascript import assign
from dash import dcc
from dash import Dash, html
from dash.dependencies import Input, Output

chroma = "https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"  # js lib used for colors

# df = pd.read_csv("/Users/xiaohan/dsa3101-2210-13-lta/backend/Model/training_data.csv")
df = pd.read_csv("/backend/Model/training_data.csv")
 
# Create the app.
app = Dash(external_scripts=[chroma], prevent_initial_callbacks=True)

app.layout = html.Div([
    html.Div(
        children=[
            html.H3('Select what you would like to view.'),
            # Add a dropdown with identifier
            dcc.Dropdown(id = 'aggregation',
            options=[
                {'label':'Max Traffic Density', 'value': 'Max Traffic Density'},
                {'label':'Mean Traffic Density', 'value': 'Mean Traffic Density'},
                {'label':'Min Traffic Density', 'value': 'Min Traffic Density'}],
                style={'width':'200px', 'margin':'0 auto', 'display': 'inline-block'})
            ],
            style={'width':'500px', 'height':'200px', 'vertical-align':'top',
                   'padding':'20px', 'margin':'auto', 'display':'flex','align-items': 'center'}),
    html.Div(id = 'variable',
        style = {'width':'90%', 'height':'80vh', 'margin':'0 auto', 'position':'relative'})
    ])

@app.callback(
    Output(component_id = 'variable', component_property = 'children'),
    Input(component_id = 'aggregation', component_property = 'value')
    )

def update_map(input_selected):
    variable = 'All Variables'
    point_to_layer = assign("""function(feature, latlng, context){
    const {min, max, colorscale, circleOptions, colorProp} = context.props.hideout;
    const csc = chroma.scale(colorscale).domain([min, max]);  // chroma lib to construct colorscale
    circleOptions.fillColor = csc(feature.properties[colorProp]);  // set color based on color prop.
    return L.circleMarker(latlng, circleOptions);  // sender a simple circle marker.
    }""")
    
    if input_selected == 'Max Traffic Density':
        color_prop0 = 'Density'
        colorscale0 = ['green','yellow','orange','red'] 
        df0 = df.sort_values('Density', ascending = False).drop_duplicates(subset='Camera_Id').sort_index()
        df0= df0[['Latitude', 'Longitude', 'Direction', 'Camera_Id', 'Jam',color_prop0, 'Time']]
        dicts0 = df0.to_dict('records')
        for item in dicts0:
            item["tooltip"] = 'Camera {}: Traffic density along {} is {:.2f}'.format(item['Camera_Id'], item['Direction'], item[color_prop0]) # bind tooltip max
        geojson0 = dlx.dicts_to_geojson(dicts0, lon="Longitude", lat="Latitude")
        geobuf0 = dlx.geojson_to_geobuf(geojson0)
        vmax0 = df[color_prop0].max()
        colorbar0 = dl.Colorbar(colorscale=colorscale0, width=20, height=150, min=0, max=vmax0, unit='Traffic density per lane', opacity=0.9)
        geojson0 = dl.GeoJSON(data=geobuf0, id="geojson", format="geobuf",
                     zoomToBounds=True,  # when true, zooms to bounds when data changes
                     options=dict(pointToLayer=point_to_layer),  # how to draw points
                     superClusterOptions=dict(radius=50),   # adjust cluster size
                     hideout=dict(colorProp=color_prop0, circleOptions=dict(fillOpacity=0.7, stroke=False, radius=7),
                                  min=0, max=vmax0, colorscale=colorscale0))
        map = dl.Map([dl.TileLayer(url='https://maps-{s}.onemap.sg/v3/Grey/{z}/{x}/{y}.png', id= 'variable',maxZoom=13, minZoom=12,
                             attribution='<img src="https://www.onemap.gov.sg/docs/maps/images/oneMap64-01.png" style="height:20px;width:20px;"/> OneMap | Map data &copy; contributors, <a href="http://SLA.gov.sg">Singapore Land Authority</a>'),
    geojson0, colorbar0], center=[1.3521, 103.8198],
                          style={'width': '90%', 'height': '80vh', 'margin': "auto", "display": "block", "position": "relative"},)
        
    elif input_selected == 'Min Traffic Density':
        color_prop0 = 'Density'
        colorscale0 = ['green','yellow','orange','red'] 
        df0 = df.sort_values('Density', ascending = True).drop_duplicates(subset='Camera_Id').sort_index()
        df0= df0[['Latitude', 'Longitude', 'Direction', 'Camera_Id', 'Jam',color_prop0, 'Time']]
        dicts0 = df0.to_dict('records')
        for item in dicts0:
            item["tooltip"] = 'Camera {}: Traffic density along {} is {:.2f}'.format(item['Camera_Id'], item['Direction'], item[color_prop0]) # bind tooltip max
        geojson0 = dlx.dicts_to_geojson(dicts0, lon="Longitude", lat="Latitude")
        geobuf0 = dlx.geojson_to_geobuf(geojson0)
        vmax0 = df[color_prop0].max()
        colorbar0 = dl.Colorbar(colorscale=colorscale0, width=20, height=150, min=0, max=vmax0, unit='Traffic density per lane', opacity=0.9)
        geojson0 = dl.GeoJSON(data=geobuf0, id="geojson", format="geobuf",
                    zoomToBounds=True,  # when true, zooms to bounds when data changes
                    options=dict(pointToLayer=point_to_layer),  # how to draw points
                    superClusterOptions=dict(radius=50),   # adjust cluster size
                    hideout=dict(colorProp=color_prop0, circleOptions=dict(fillOpacity=0.7, stroke=False, radius=7),
                              min=0, max=vmax0, colorscale=colorscale0))
        map = dl.Map([dl.TileLayer(url='https://maps-{s}.onemap.sg/v3/Grey/{z}/{x}/{y}.png', id= 'variable',maxZoom=13, minZoom=12,
                             attribution='<img src="https://www.onemap.gov.sg/docs/maps/images/oneMap64-01.png" style="height:20px;width:20px;"/> OneMap | Map data &copy; contributors, <a href="http://SLA.gov.sg">Singapore Land Authority</a>'),
    geojson0, colorbar0], center=[1.3521, 103.8198],
                          style={'width': '90%', 'height': '80vh', 'margin': "auto", "display": "block", "position": "relative"},)
        
    elif input_selected == 'Mean Traffic Density':
        color_prop0 = 'Density'
        colorscale0 = ['green','yellow','orange','red'] 
        df0 = df.groupby(['Camera_Id', 'Longitude','Latitude','Time'])['Density'].mean().reset_index()
        df0= df0[['Latitude', 'Longitude', 'Camera_Id', 'Jam',color_prop0, 'Time']]
        dicts0 = df0.to_dict('records')
        for item in dicts0:
            item["tooltip"] = 'Camera {}: Average traffic density is {:.2f}'.format(item['Camera_Id'], item[color_prop0]) # bind tooltip max
        geojson0 = dlx.dicts_to_geojson(dicts0, lon="Longitude", lat="Latitude")
        geobuf0 = dlx.geojson_to_geobuf(geojson0)
        vmax0 = df[color_prop0].max()
        colorbar0 = dl.Colorbar(colorscale=colorscale0, width=20, height=150, min=0, max=vmax0, unit='Traffic density', opacity=0.9)
        geojson0 = dl.GeoJSON(data=geobuf0, id="geojson", format="geobuf",
                    zoomToBounds=True,  # when true, zooms to bounds when data changes
                    options=dict(pointToLayer=point_to_layer),  # how to draw points
                    superClusterOptions=dict(radius=50),   # adjust cluster size
                    hideout=dict(colorProp=color_prop0, circleOptions=dict(fillOpacity=0.7, stroke=False, radius=7),
                              min=0, max=vmax0, colorscale=colorscale0))
        map = dl.Map([dl.TileLayer(url='https://maps-{s}.onemap.sg/v3/Grey/{z}/{x}/{y}.png', id= 'variable',maxZoom=13, minZoom=12,
                             attribution='<img src="https://www.onemap.gov.sg/docs/maps/images/oneMap64-01.png" style="height:20px;width:20px;"/> OneMap | Map data &copy; contributors, <a href="http://SLA.gov.sg">Singapore Land Authority</a>'),
    geojson0, colorbar0], center=[1.3521, 103.8198],
                          style={'width': '90%', 'height': '80vh', 'margin': "auto", "display": "block", "position": "relative"},)
    return map

if __name__ == '__main__':
    app.run_server(port = 8080, threaded= True)


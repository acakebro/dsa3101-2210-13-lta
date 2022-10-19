'''
 # @ Create Time: 2022-10-08 23:39:32.168931
'''

from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from datetime import datetime, date
import dash_leaflet as dl


app = Dash(__name__, title="frontend")

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

traffic_incidents = pd.read_csv("traffic_incidents.csv")
traffic_speedbands = pd.read_csv("traffic_speedbands.csv")
traffic_images = pd.read_csv("traffic_images.csv")

cameras = [dict(title = str(traffic_images['CameraID'][0]),
                position = [traffic_images['Latitude'][0],traffic_images['Longitude'][0]])]

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
fig.update_layout({'paper_bgcolor':'rgb(237,250,252)'})


#maps = px.scatter_geo(traffic_images, lon = "Longitude",
 #                     lat = "Latitude",
 #                     scope = "asia")

#maps.update_layout({
#    'geo': {
#        'resolution': 50
#    }
#})

d_table_in = dash_table.DataTable(
            data=traffic_incidents.to_dict('records'),
            columns = [{"name": i, "id": i} for i in traffic_incidents.columns[:len(traffic_incidents.columns)-1]],
            cell_selectable=False,
            sort_action='native',
            filter_action='native',
            page_action = 'native',
            page_current = 0,
            page_size = 10
            )

d_table_sp = dash_table.DataTable(
            data=traffic_speedbands.to_dict('records'),
            columns = [{"name": i, "id": i} for i in traffic_speedbands.columns],
            cell_selectable=False,
            sort_action='native',
            filter_action='native',
            page_action = 'native',
            page_current = 0,
            page_size = 10
            )

d_table_im = dash_table.DataTable(
            data=traffic_images.to_dict('records'),
            columns = [{"name": i, "id": i} for i in traffic_images.columns],
            cell_selectable=False,
            sort_action='native',
            filter_action='native',
            page_action = 'native',
            page_current = 0,
            page_size = 10
            )

app.layout = html.Div(children=[
    html.H1(children='Title', style = {'text-align':'center'}),
    html.Br(),

    # filter box
    html.Div(children = [
    html.H2("Select date: ", style = {'display': 'inline-block', 'margin':'5px'}),
    dcc.DatePickerSingle(id = "traffic_date",
                         min_date_allowed = date(2022,1,1),
                         max_date_allowed = date.today(),
                         date = date.today(),
                         initial_visible_month = date.today(),
                         style = {'display': 'inline-block', 'width':'10px',
                                  'margin':'5px auto'}),
    html.Br(),
    html.H2("Select road: ", style = {'display': 'inline-block', 'margin':'5px'}),
    dcc.Dropdown(id = "road_name",
                 options = [
            {'label':'Road A', 'value':'Road A'},
            {'label':'Road B', 'value':'Road B'},
            {'label':'Road C', 'value':'Road C'},
            {'label':'Road D', 'value':'Road D'},
            {'label':'Road E', 'value':'Road E'}],
                 style = {'display': 'inline-block', 'width':'200px', 'height': '30px',
                          'margin': '5px auto'})
    ], style = {'border': '1px solid black'}
             ),

    html.Br(),

    # images
    html.Div(children = [
    dcc.Graph(
        id='example-graph1',
        figure=fig,
        style = {'display': 'inline-block', 'width': '450px'}
    ),
    
    dcc.Graph(
        id='example-graph2',
        figure=fig,
        style = {'display': 'inline-block', 'width': '450px'}
    ),
    
    dcc.Graph(
        id='example-graph3',
        figure=fig,
        style = {'display': 'inline-block', 'width': '450px'}
    ),
    
    dcc.Graph(
        id='example-graph4',
        figure=fig,
        style = {'display': 'inline-block', 'width': '450px'}
    ),
    
                        ],
             style = {'text-align':'center', 'font-size':18}
             ),

    html.Div(children = [
        dl.Map([dl.TileLayer()] + [dl.Marker(**i) for i in cameras],
               style={'width': '1000px', 'height': '500px'})
                  ]),
    

    # tables
    html.Div(children = [
        html.H2("Traffic Incidents"),
        html.Div(d_table_in,
             style = {'width':'100%', 'height':'350px',
                      'margin':'10px auto', 'padding-right':'30px'}),
        html.H2("Traffic Speedbands"),
        html.Div(d_table_sp,
             style = {'width':'100%', 'height':'350px',
                      'margin':'10px auto', 'padding-right':'30px'}),
        html.H2("Traffic Images"),
        html.Div(d_table_im,
             style = {'width':'100%', 'height':'350px',
                      'margin':'10px auto', 'padding-right':'30px'})
    
        ])
    ],
                      style = {'background-color': 'rgb(237,250,252)'}
                      )




if __name__ == '__main__':
    app.run_server(debug=True)


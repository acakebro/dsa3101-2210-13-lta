'''
 # @ Create Time: 2022-10-08 23:39:32.168931
'''

from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from datetime import datetime, date
import dash_leaflet as dl
import plotly.graph_objects as go

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
train_data = pd.read_csv("train_data.csv")

#cameras = [dict(title = str(traffic_images['CameraID'][0]),
#                position = [traffic_images['Latitude'][0],traffic_images['Longitude'][0]])]

cameras = [dict(center = [traffic_images['Latitude'][i],traffic_images['Longitude'][i]],
                children = [dl.Tooltip("Camera ID: " + str(traffic_images['CameraID'][i])), dl.Popup('Circle marker, 20px')],
               ) for i in range(len(traffic_images))]

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

def create_n_Img(link, n):
    # Add a component that will render an image
    img = html.Img(
        src=link, 
        # Add the corporate styling
        style = {'display': 'inline-block', 'width': '450px'})
    img_list = [img] * n
    return img_list
'''
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
'''
layout = html.Div(children=[
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
    html.H2("Select expressway: ", style = {'display': 'inline-block', 'margin':'5px'}),
    dcc.Dropdown(id = "exp_dd",
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
    *create_n_Img("assets/1001_2043_20221009204509_554949.jpg", 2),
    
    html.Img(src = "assets/1001_2043_20221009204509_554949.jpg"),
    html.Img(src = "images/2022_10_20_11_55/1001_1148_20221020115515_535455.jpg"),
    
    
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
    
    # map
    html.Div(children = [
        dl.Map(children = [dl.TileLayer()] + [dl.CircleMarker(**i) for i in cameras],
               style={'width': '1000px', 'height': '500px'},
              center=[1.3521, 103.8198],
              zoom = 11)
                  ]),
    

    ],
                      style = {'background-color': 'rgb(237,250,252)'}
                      )

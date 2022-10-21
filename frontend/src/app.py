'''
 # @ Create Time: 2022-10-08 23:39:32.168931
'''

import sys
import pathlib

sys.path.insert(1, "../../backend/Model/")


from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
import sys
from api_calls import ApiCall
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from datetime import datetime, date
import dash_leaflet as dl
import os
from api_calls import ApiCall

api_obj = ApiCall("../src")
api_obj.download_images()

app = Dash(__name__, title="frontend")

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server


traffic_incidents = pd.read_csv("traffic_incidents.csv")
traffic_speedbands = pd.read_csv("traffic_speedbands.csv")
traffic_images = pd.read_csv("traffic_images.csv")
train_data = pd.read_csv("../interface/train_data.csv")

#cameras = [dict(title = str(traffic_images['CameraID'][0]),
#                position = [traffic_images['Latitude'][0],traffic_images['Longitude'][0]])]

cameras = [dict(center = [traffic_images['Latitude'][i],traffic_images['Longitude'][i]],
                children = [dl.Tooltip("Camera ID: " + str(traffic_images['CameraID'][i])), dl.Popup('Circle marker, 20px')],
               ) for i in range(len(traffic_images))]

folder = "assets/"

def create_Img(link_list):
    # Add a component that will render an image
    img_list = [html.Img(
        title = str(link_list[i][:4]),
        src= folder + link_list[i],
        style = {'display': 'inline-block', 'width': '450px',
                 'margin': '20px'}) for i in range(len(link_list))]
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
app.layout = html.Div(children=[
    html.H1(children='Title', style = {'text-align':'center'}),
    html.Br(),

    # filter box
    html.Div(children = [
    html.H2("Select date: ", style = {'margin':'5px'}),
    dcc.DatePickerSingle(id = "traffic_date",
                         min_date_allowed = date(2022,1,1),
                         max_date_allowed = date.today(),
                         date = date.today(),
                         initial_visible_month = date.today(),
                         style = {'display': 'inline-block', 'width':'10px',
                                  'margin':'10px auto'}),
    html.Br(),
    html.H2("Select expressway: ", style = {'margin':'5px'}),
    dcc.Dropdown(id = "exp_dd",
                 options = [
            {'label':'Road A', 'value':'Road A'},
            {'label':'Road B', 'value':'Road B'},
            {'label':'Road C', 'value':'Road C'},
            {'label':'Road D', 'value':'Road D'},
            {'label':'Road E', 'value':'Road E'}],
                 style = {'display': 'inline-block', 'width':'200px', 'height': '30px',
                          'margin': '10px auto'})
    ], style = {'border': '1px solid black', 'width': '20%'}
             ),

    html.Br(),

    # images
    html.Div(children = [
    *create_Img(os.listdir(folder))],
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

'''
@app.callback(
    Output(component_id='graph1', component_property='figure'),
    Input(component_id='exp_dd', component_property='value')
)


def filter_image(input_exp):
    exp_filter = 'All Countries'
    sales = ecom_sales.copy(deep=True)
    if input_country:
        country_filter = input_country
        sales = sales[sales['Country'] == country_filter]
    ecom_bar_major_cat = sales.groupby('Major Category')['OrderValue'].agg('sum').reset_index(name='Total Sales ($)')
    bar_fig_major_cat = px.bar(
        title=f'Sales in {country_filter}', data_frame=ecom_bar_major_cat, x='Total Sales ($)', y='Major Category', color='Major Category',
                 color_discrete_map={'Clothes':'blue','Kitchen':'red','Garden':'green','Household':'yellow'})
    return bar_fig_major_cat
'''


#if __name__ == '__main__':
#    app.run_server(debug=True)


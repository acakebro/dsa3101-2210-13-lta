import dash
import os
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import numpy as np
from os import listdir
from dash.dependencies import Input, Output
from PIL import Image

image_folder="assets"
directory = os.fsencode(image_folder)

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
    #Road Dropdown
    html.Div(
        children=[
        html.Label(['Road:'], style={'font-weight': 'bold', 'text-align': 'center'}),

        dcc.Dropdown(id='road_label',
        options=[
            {'label':'ECP', 'value':'East Coast Parkway'},
            {'label':'KPE', 'value':'Kallang-Paya Lebar Expressway'},
            {'label':'PIE', 'value':'Pan-Island Expressway'},
            {'label':'MCE', 'value':'Marina Coastal Expressway'},
            {'label':'SLE', 'value':'Seletar Expressway'},
            {'label':'BKE', 'value':'Bukit Timah Expressway'},
            {'label':'KJE', 'value':'Kranji Expressway'},
            {'label':'CTE', 'value':'Central Expressway'},
            {'label':'TPE', 'value':'Tampines Expressway'},
            {'label':'AYE', 'value':'Ayer Rajah Expressway'},
            {'label':'Woodlands', 'value':'Woodlands Checkpoint'},
            {'label':'Tuas', 'value':'Tuas Checkpoint'}],
            placeholder="Select road...",
            style={'width':'150px', 'margin':'0 auto','text-align': 'left'})],
        style={'width':'250px', 'height':'50px','vertical-align':'center',
            'padding':'10px'}),
    #Camera ID and DateTime dropdown
    html.Div(
        children=[
        html.Div(
            children=[
            html.Label(['Camera ID:'], style={'font-weight': 'bold', "text-align": "left"}),
            dcc.Dropdown(id='camera_id',
            options=[
                {'label':'1001', 'value':'1001'},
                {'label':'1002', 'value':'1002'},
                {'label':'1003', 'value':'1003'}],
                placeholder='Select Camera ID',
                style={'width':'150px', 'margin':'0 auto','text-align': 'left'})],
            style={'width':'350px', 'height':'50px','vertical-align':'left','display':'inline-block',
                'padding':'10px'}),
        html.Div(
            children=[
            html.Label(['DateTime:'], style={'font-weight': 'bold', "text-align": "right"}),
            dcc.Dropdown(id='datetime',
            options=[
                {'label':'20221009204509', 'value':'20221009204509'},
                {'label':'20221009204507', 'value':'20221009204507'},
                {'label':'20221009204506', 'value':'20221009204506'}],
                placeholder='Select DateTime',
                style={'width':'150px', 'margin':'0 auto','text-align': 'left'})],
            style={'width':'350px', 'height':'50px','vertical-align':'right','display':'inline-block',
                'padding':'10px'})]),
    html.Br(),
    html.Br(),
    #Image after filter
    html.Div(id='img')
    ])

@app.callback(
[Output('img','children')],
[Input('camera_id','value'),
 Input('datetime','value')])

def filter_image(camera_id,datetime):
    if camera_id is None or datetime is None:
            raise dash.exceptions.PreventUpdate
    for filename in os.listdir(directory):
        file = os.fsdecode(filename)
        if camera_id in file and datetime not in file:
            raise dash.exceptions.PreventUpdate
        if camera_id not in file and datetime in file:
            raise dash.exceptions.PreventUpdate
        if camera_id in file and datetime in file:
            return [html.Img(src=image_folder+'/'+file)]

if __name__ == '__main__':
    app.run_server(debug=True,port=8051)


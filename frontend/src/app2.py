import dash
import os
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import numpy as np
from os import listdir
from dash.dependencies import Input, Output
from datetime import datetime, date

image_folder="assets"
directory = os.fsencode(image_folder)

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
    #Road Dropdown
    html.Div(
        children=[
        html.Label(['Road:'], style={'font-weight': 'bold'}),
        dcc.Dropdown(id='road_name',
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
                        {'label':'Tuas', 'value':'Tuas Checkpoint'}
                        ],
                    placeholder="Select road...",
                    style={'width':'150px','margin':'20px'})
        ],
        style = {'width':'100%','display':'flex','align-items':'center','justify-content':'center'}
        ),
    
    html.Div(
        children=[
        #Camera ID dropdown
        html.Div(
            children=[
            html.Label(['Camera ID:'], style={'font-weight': 'bold'}),
            dcc.Dropdown(id='camera_id',
                        options=[
                            {'label':'1001', 'value':'1001'},
                            {'label':'1002', 'value':'1002'},
                            {'label':'1003', 'value':'1003'},
                            {'label':'1501', 'value':'1501'},
                            {'label':'1502', 'value':'1502'}
                            ],
                        placeholder='Select Camera ID...',
                        style={'width':'170px', 'margin':'20px'})
            ],
            style={'margin':'20px'}
            ),
        html.Div(
            children=[
            #Date pick
            html.Label(['Date:'], style={'font-weight': 'bold'}),
            dcc.DatePickerSingle(id = "traffic_date",
                                 min_date_allowed = date(2022,1,1),
                                 max_date_allowed = date.today(),
                                 date = date.today(),
                                 initial_visible_month = date.today(),
                                 style = {'display': 'inline-block', 'width':'150px','margin':'20px'}
                                 )
            ]),
        html.Div(
            children=[
            #Time input
            html.Label(['Time:'], style={'font-weight': 'bold'}),
            dcc.Input(id="traffic_time",
                      type="number",
                      placeholder="HHMM",
                      style = {'display': 'inline-block', 'width':'60px','margin':'20px'})
            ])
        
        ],
        style = {'width':'100%','display':'flex','align-items':'center','justify-content':'center'}
        ),
    
    html.Br(),
    html.Br(),
    
    html.Div(
            children=[
            #Image after filter
            html.Div(id='img',style={'display':'inline-block'}),
            #Prediction attributes
            html.Div(
                children=[
                html.H3('Density:', style={'font-weight': 'bold'}),
                html.H3('Speed:', style={'font-weight': 'bold'}),
                html.H3('Traffic condition:', style={'font-weight': 'bold'}),
                html.H3('Traffic condition:', style={'font-weight': 'bold'})
                ],
                style={'display':'none','padding':'20px','text-align': 'right'},
                id='attributes'
                )
            ],
            style = {'display':'flex','align-items':'center','justify-content':'center'}
            )
    ])

    #Graphs
#    html.Div(children = [
#    dcc.Graph(
#        id='example-graph1',
#        figure=fig,
#        style = {'display': 'inline-block', 'width': '450px'}
#    ),
#    
#    dcc.Graph(
#        id='example-graph2',
#        figure=fig,
#        style = {'display': 'inline-block', 'width': '450px'}
#    ),
#    
#    dcc.Graph(
#        id='example-graph3',
#        figure=fig,
#        style = {'display': 'inline-block', 'width': '450px'}
#   ),
#
#    dcc.Graph(
#        id='example-graph4',
#        figure=fig,
#        style = {'display': 'inline-block', 'width': '450px'}
#    ),
#    
#                        ],
#             style = {'text-align':'center', 'font-size':18}
#             ),


@app.callback(
[Output('img','children'),
Output('attributes','style')],
[Input('camera_id','value'),
 Input('traffic_date','date'),
 Input('traffic_time','value')])

def update_output(camera_id,traffic_value,time):
    #Stop update if missing values
    if traffic_value is not None:
        date_object = date.fromisoformat(traffic_value)
        datetime = date_object.strftime('%Y%m%d')
    if camera_id is None or datetime is None:
        raise dash.exceptions.PreventUpdate
    if time is not None and len(str(time))!=4:
        raise dash.exceptions.PreventUpdate
    #Make hidden attributes appear
    attributes_style={'display':'inline-block','padding':'20px','text-align': 'right'}
    datetime+=str(time)
    #Search for image by datetime and camera_id
    for filename in os.listdir(directory):
        file = os.fsdecode(filename)
        print(file)
        if camera_id in file and datetime not in file:
            raise dash.exceptions.PreventUpdate
        if camera_id in file and datetime in file:
            return [html.Img(src=image_folder+'/'+file)],attributes_style

if __name__ == '__main__':
    app.run_server(debug=True,port=8052)



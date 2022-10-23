import pandas as pd 
import dash
import os
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import numpy as np
from os import listdir
from dash.dependencies import Input, Output
from datetime import datetime, date,timedelta
from time import strftime,localtime

layout = html.Div(
    children=[
    #Road Dropdown
    html.Div(
        children=[
        html.H2('Road:', style={'font-weight': 'bold'}),
        dcc.Dropdown(id='road_name',
                    options=[
                        {'label':'ECP', 'value':'ECP'},
                        {'label':'KPE', 'value':'KPE'},
                        {'label':'PIE', 'value':'PIE'},
                        {'label':'MCE', 'value':'MCE'},
                        {'label':'SLE', 'value':'SLE'},
                        {'label':'BKE', 'value':'BKE'},
                        {'label':'KJE', 'value':'KJE'},
                        {'label':'CTE', 'value':'CTE'},
                        {'label':'TPE', 'value':'TPE'},
                        {'label':'AYE', 'value':'AYE'}
                        ],
                    placeholder="Select road...",
                    style={'width':'150px','margin':'20px'})
        ],
        style = {'width':'100%','display':'flex','align-items':'center','justify-content':'center'}
        ),

    #2nd row dropdowns
    html.Div(
        children=[
        #Camera ID dropdown
        html.Div(
            children=[
            html.H2('Camera ID:', style={'font-weight': 'bold'}),
            dcc.Dropdown(id='camera_id',
                        options=[
                            {'label':'1001', 'value':'1001'},
                            {'label':'1002', 'value':'1002'},
                            {'label':'1003', 'value':'1003'},
                            {'label':'1501', 'value':'1501'},
                            {'label':'1502', 'value':'1502'}
                            ],
                        placeholder='Select Camera ID...',
                        style={'width':'170px', 'margin':'10px','display': 'inline-block'})
            ],
            style ={'width':'400px'}
            ),

        #Date pick
        html.Div(
            children=[
            html.H2('Date:', style={'font-weight': 'bold'}),
            dcc.DatePickerSingle(id = "traffic_date",
                                 min_date_allowed = date(2022,1,1),
                                 max_date_allowed = date.today(),
                                 date = date.today(),
                                 initial_visible_month = date.today(),
                                 style = {'display': 'inline-block', 'width':'150px','margin':'20px'}
                                 )
            ],style ={'width':'400px'}),

        #Time input
        html.Div(
            children=[
            html.H2('Time:', style={'font-weight': 'bold'}),
            dcc.Input(id="traffic_time",
                      type="text",
                      placeholder="HHMM",
                      value=strftime("%H%M", localtime()),
                      style = {'display': 'inline-block', 'width':'100px','height':'30px','margin':'25px'})
            ])
        
        ],
        style = {'width':'100%','display':'flex','align-items':'center','justify-content':'center'}
        ),
    
    html.Br(),
    html.Br(),

    #Image and predictions
    html.Div(
            children=[
            #Image after filter
            html.Div(id='img',style={'display':'inline-block'}),
            #Prediction attributes
            html.Div(
                children=[
                html.H2('Density:', style={'font-weight': 'bold'}),
                html.H2('Speed:', style={'font-weight': 'bold'}),
                html.H2('Traffic condition:', style={'font-weight': 'bold'}),
                html.H2('Traffic condition:', style={'font-weight': 'bold'})
                ],
                style={'display':'none','padding':'20px','text-align': 'right'},
                id='attributes'
                )
            ],    
            style = {'display':'flex','align-items':'center','justify-content':'center'}
            ),


    #Data visualization
    html.Div(children = [
        html.H2('Past data analysis', style={'font-weight': 'bold'}),
        dcc.Dropdown(id='timeframe',
                        options=[
                            {'label':'last 30 minutes', 'value':'30'},
                            {'label':'last 1 hour', 'value':'60'}
                            ],
                     style = {'margin':'20px'}),
        dcc.Graph(
            id='speed',
            style = {'display': 'inline-block', 'width': '450px'}
        ),       
        dcc.Graph(
            id='density',
            style = {'display': 'inline-block', 'width': '450px'}
        )
        ])
        
        ],
    style = {'background-color': 'rgb(237,250,252)'})


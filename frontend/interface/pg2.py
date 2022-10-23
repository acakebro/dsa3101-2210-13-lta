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

layout = html.Div(
    children=[
    #Road Dropdown
    html.Div(
        children=[
        html.Label(['Road:'], style={'font-weight': 'bold'}),
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
            html.Label(['Camera ID:'], style={'font-weight': 'bold'}),
            dcc.Dropdown(id='camera_id',
                        placeholder='Select Camera ID...',
                        style={'width':'170px', 'margin':'20px'})
            ],
            style={'margin':'20px'}
            ),

        #Date pick
        html.Div(
            children=[
            html.Label(['Date:'], style={'font-weight': 'bold'}),
            dcc.DatePickerSingle(id = "traffic_date",
                                 min_date_allowed = date(2022,1,1),
                                 max_date_allowed = date.today(),
                                 date = date.today(),
                                 initial_visible_month = date.today(),
                                 style = {'display': 'inline-block', 'width':'150px','margin':'20px'}
                                 )
            ]),

        #Time input
        html.Div(
            children=[
            html.Label(['Time:'], style={'font-weight': 'bold'}),
            dcc.Input(id="traffic_time",
                      type="number",
                      placeholder="HHMM",
                      style = {'display': 'inline-block', 'width':'100px','margin':'20px'})
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
                html.H3('Density:'),
                html.H3('Speed:'),
                html.H3('Traffic condition:'),
                html.H3('Traffic condition:')
                ],
                style={'display':'none','padding':'20px','text-align': 'right'},
                id='attributes'
                )
            ],
            style = {'display':'flex','align-items':'center','justify-content':'center','font_size': '12px'}
            ),


    #Data visualization
    html.Div(children = [
        html.Label(['Past data analysis'], style={'font-weight': 'bold'}),
        dcc.Dropdown(id='timeframe',
                     placeholder="last 4 hours",
                        options=[
                            {'label':'last 30 minutes', 'value':'30'},
                            {'label':'last 1 hour', 'value':'60'}
                            ]),
        dcc.Graph(
            id='speed',
            style = {'display': 'inline-block', 'width': '450px'}
        ),       
        dcc.Graph(
            id='density',
            style = {'display': 'inline-block', 'width': '450px'}
        )
        ])
        ])
    


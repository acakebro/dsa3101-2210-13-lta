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
                        placeholder='1001',
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
                html.H2('Direction:', style={'font-weight': 'bold'}),
                html.H2('Density:', style={'font-weight': 'bold'}),
                html.H2('Speed:', style={'font-weight': 'bold'}),
                html.H2('Traffic condition:', style={'font-weight': 'bold'}),
                ],
                style={'display':'none','padding':'20px','text-align': 'right'},
                id='attributes'
                ),
            html.Div(id = 'datatable')
            ],    
            style = {'display':'flex','align-items':'center','justify-content':'center'}
            ),


    #Data visualization
    html.Div(children = [
        html.Div(children = [
            html.H2('Past data analysis', style={'font-weight': 'bold'}),
            dcc.Dropdown(id='timeframe',
                            options=[
                                {'label':'last 30 minutes', 'value':'30'},
                                {'label':'last 1 hour', 'value':'60'}
                                ],
                         placeholder='last 15 minutes',
                         style = {'margin':'20px','width':'200px'}
                         ),
            dcc.Graph(
                id='speed',
                style = {'display': 'inline-block', 'width': '450px'}
                ),       
            dcc.Graph(
                id='density',
                style = {'display': 'inline-block', 'width': '450px'}
                )
            ],
            )
        ],
        style = {'display':'flex','align-items':'center','justify-content':'center'}
        ),
    html.Div(children = [
            html.H2('Congested areas(> 2 hours of continuous jam)',
                    style={'font-weight': 'bold'}
                    ),
            html.Div(id = 'places')
            ],
            style = {'width': '700px','margin':'auto'}
            ),
    html.A(html.Button('Refresh Page'),
            href='/page2'
           )
    ],
    style = {'background-color': 'rgb(237,250,252)'}
    )


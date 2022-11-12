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

d_exp_cam = {
        'KPE': ['1001', '1002', '1003', '1004', '1005', '1006', '7793',
                     '7794', '7795'],
        'ECP': ['1001', '1002', '1003', '1004', '1005', '1006', '1501', '1503',
                '1505', '7791'],
        'KJE': ['2708', '6714'],
        'SLE': ['1701', '1702', '1703', '1704', '1705', '1706', '1707', '1709',
               '1711', '7791', '7793', '7795', '7796', '7797'],
        'MCE': ['1501', '1502', '1503', '1504', '1505', '4704'],
        'CTE': ['1705', '4704', '7797', '7798'], 
        'TPE': ['1001', '1003', '1005', '1006', '7798', '9701', '9702', '9703',
                '9704', '9705', '9706'], 
        'BKE': ['2702', '7798', '8701', '8702', '8704', '8706', '9701', '9702',
                '9703', '9704', '9705', '9706'], 
        'PIE': ['1002', '1003', '1004', '1703', '2703', '2705', '2706', '2707',
                '2708', '7791', '7793', '7794', '7795', '7796', '7797', '8701',
                '8702', '8704', '8706', '9703'],  
        'AYE': ['1502', '1503', '1504', '1703', '1704', '1706', '1707', '3795',
                '3796', '4713', '6716'],
        'Woodlands Causeway/Johor': ['2701', '2702', '2703', '2704', '2705',
                                     '2706', '2707', '2708', '9703'], 
        'Tuas/Johor': ['1002', '1004', '1703', '4703', '4707', '4712', '4713',
                       '6708', '6715', ],
        'Changi': ['1001', '1002', '1003', '1703', '2703', '3704', '3793', '3796',
                   '3797', '3798', '4702', '5794', '5795', '5797', '5798', '5799',
                   '6701', '6703', '6704', '6705', '6706', '6708', '6710', '6712',
                   '6713', '6714', '6715', '6716'],
        'City': ['1001', '1701', '1702', '1709', '1711', '3702', '3704', '3705',
                 '3793', '3795', '3796', '3797', '3798', '4701', '4705', '4707',
                 '4708', '4709', '4710', '4712', '4716', '6711'],
        'Moulmein': ['1701'],
        'Yio Chu Kang': ['1706'],
        'Jalan Bukit Merah': ['1707'],
        'Jurong' : ['2703', '4701', '4702', '4705', '4706', '4709', '4710', '4714',
                    '4716', '5794', '5795', '5797', '5798', '5799', '6701', '6703',
                    '6704', '6705', '6706', '6710', '6711', '6712', '6713'],
        'Airport' : ['3702', '3705', '6711'],
        'Xilin Ave': ['3705'],
        'Marine Parade': ['3795'],
        'Telok Blangah': ['4798', '4799'],
        'Sentosa': ['4799'],
        'Toa Payoh': ['6701'],
        'Thomson': ['6703'],
        'Pasir Ris Dr 12': ['7793'],
        'Punggol/Sengkang': ['7796'],
        'Choa Chu Kang': ['8701', '8704'],
        'Woodlands Ave 2': ['9705']
             }

def road_options(cam):
    options=[]
    for road in d_exp_cam.keys():
        options+=[{'label':str(road), 'value':str(road)}]
    return options

layout = html.Div(
    children=[
    #Road Dropdown
    html.Div(
        children=[
        html.H2('Road:', style={'font-weight': 'bold'}),
        dcc.Dropdown(id='road_name',
                    options=road_options(d_exp_cam),
                    placeholder='KPE',
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

    #Image and statistics
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
                style={'padding':'20px','text-align': 'right'},
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
                                {'label':'last 4 hour', 'value':'240'},
                                {'label':'last 2 hour', 'value':'120'},
                                {'label':'last 1 hour', 'value':'60'}],
                         placeholder='last 1 hour',
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
    #Congested areas table
    html.Div(children = [
            html.H2('Congested areas(> 2 hours of continuous jam)',
                    style={'font-weight': 'bold'}
                    ),
            html.Div(id = 'places')
            ],
            style = {'width': '700px','margin':'auto'}
            ),
    ],
    style = {'background-color': 'white'}
    )


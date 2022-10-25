import dash
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from os import listdir
from dash.dependencies import Input, Output
from datetime import datetime, date,timedelta
from time import localtime, strftime
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc

app = Dash(__name__, title="frontend")

app.layout = html.Div(
    children=[
    html.H2("Prediction of traffic condition in 30 days", style={'align-items':'center'}),
    html.H3("Please choose the camera, road, day, and time you would like to view."),
    html.Div(
        # Camera dropdown
        children = [
        html.H3('Select camera', style={'font-weight': 'bold'}),
        dcc.Dropdown(id='camera_id',
                        placeholder='1001',
                        style={'width':'170px', 'margin':'10px','display': 'inline-block'})
            ],
        style = {'width':'100%','display':'flex','align-items':'center','justify-content':'center'}),
    html.Div(
        # Road dropdown
        children = [
        html.H3('Select road', style={'font-weight': 'bold'}),
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
                {'label':'AYE', 'value':'AYE'}],
                placeholder="Select road...",
                style={'width':'150px','margin':'20px'})
        ],
        style = {'width':'100%','display':'flex','align-items':'center','justify-content':'center'}),

    #Date pick
    html.Div(
        children=[
        html.H3("Select date", style={'font-weight': 'bold'}),
        dcc.DatePickerSingle(id = "traffic_date",
                                min_date_allowed = date.today(),
                                max_date_allowed = date.today()+timedelta(days=30),
                                # date = date.today(),
                                initial_visible_month = date.today(),
                                placeholder='DD/MM/YYYY',
                                style = {'width':'150px','margin':'20px'})
        ],
        style ={'width':'100%','display':'flex','align-items':'center','justify-content':'center'}),

    #Time input
    html.Div(
        children=[
        html.H3('Select time of the day', style={'font-weight': 'bold'}),
        dcc.Input(id="traffic_time",
                      type="text",
                      placeholder="HHMM",
                      #value=strftime("%H%M", localtime()),
                      style = {'display': 'inline-block', 'width':'100px','height':'30px','margin':'25px'})
        ],
        style = {'width':'100%','display':'flex','align-items':'center','justify-content':'center'}),
    ], style={'text-align':'center', 'display':'inline-block', 'width':'100%'})


    # predictions
    #html.H3("Here is the prediction for the road condition.")

                         

if __name__ == '__main__':
    app.run_server(debug=True, port=8054)

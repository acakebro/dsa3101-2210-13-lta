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

data = pd.read_csv("train_data.csv")

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
                        style={'width':'135px','margin':'0 auto', 'display': 'inline-block'})
            ],
        style = {'width':'33.8%','margin-left':'20px','display':'flex','align-items':'center','justify-content':'center'}),
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
                style={'width':'134px','margin':'0 auto'})
        ],
        style = {'width':'35.4%','display':'flex','align-items':'center','justify-content':'center',
                 'margin-left':'20px'}),

    #Date pick
    html.Div(
        children=[
        html.H3("Select date", style={'font-weight': 'bold'}),
        dcc.DatePickerSingle(id = "traffic_date",
                                min_date_allowed = date.today(),
                                max_date_allowed = date.today()+timedelta(days=30),
                                date = date.today(),
                                initial_visible_month = date.today(),
                                placeholder='DD/MM/YYYY',
                                style = {'width':'150px','margin':'0 auto', 'border-radius': '0 auto'})
        ],
        style ={'margin-left':'20px','width':'35.5%','display':'flex','align-items':'center','justify-content':'center'}),

    #Time input
    html.Div(
        children=[
        html.H3('Select time of the day', style={'font-weight': 'bold'}),
        dcc.Input(id="traffic_time",
                      type="text",
                      placeholder="HHMM",
                      value=strftime("%H%M", localtime()),
                      style = {'width':'126px','margin':'0 auto', 'height':'30px', 'display': 'inline-block'})
        ],
        style = {'width':'29.3%','margin-left':'20px','display':'flex','align-items':'center','justify-content':'center'}),

    # predictions
    html.Div(
        children=[
        html.H3("Prediction for the road condition.", style = {'font-weight': 'bold'})],
        style={'display':'none','padding':'20px'}, id = 'attributes')

    
    ], style={'text-align':'center', 'display':'inline-block', 'width':'100%'})

@app.callback(
Output('camera_id','options'),
Input('road_name','value'))

def update_camera(road_name):
    df=data[data["Direction"]==road_name]
    return [{'label': i, 'value': str(i)} for i in df['camera_id'].unique()]

#Enter camera id,date,time and timerange to find speed and density over time of past data
@app.callback(
Output('attributes','value'),
[Input('traffic_time','value'),
 Input('traffic_date','date'),
 Input('camera_id','value'),
 Input('road_name','value')])

def prediction(camera_id, road_name, date, time):
    prediction_json = requests.get('http://0.0.0.0:5000/prediction?camera_id='+str(camera_id)+'road='+str(road_name)+'date='+str(traffic_date)+'time='+str(traffic_time)
    
    if result == 0:
        return 'No Jam'
    elif result == 1:
        return 'Jam'

                         

if __name__ == '__main__':
    app.run_server(debug=True, port=8055)

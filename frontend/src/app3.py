from dash import dcc, html, Dash, dash_table
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
from datetime import datetime, date

app = Dash(__name__, title="frontend")

app.layout = html.Div(
    html.H1("Prediction of Traffic Condition")
    children = [
        html.H2("Please choose the day, time, and road you would like to view closely."),
        html.Br(),
        html.H3("Select Day of the week"),
        # Add a dropdown for day of the week
        dcc.Dropdown(id = "Day of the Week",
                     options=[
                         {'label':'Monday', 'value': 'Monday'},
                         {'label': 'Tuesday', 'value': 'Tuesday'},
                         {'label': 'Wednesday', 'value': 'Wednesday'},
                         {'label': 'Thursday', 'value': 'Thursday'},
                         {'label': 'Friday', 'value': 'Friday'}],
                         style = {'width': '200px', 'margin':'20px'}),
        html.H3("Select Time of the day"),
        # Add a dropdown for time of the day
        dcc.Dropdown(id = "Time of the day",
                     options=[
                         {'label': '00:00', 'value': '12a.m.'},{'label': '01:00', 'value': '1a.m.'},
                         {'label': '02:00', 'value': '2a.m.'}, {'label': '03:00', 'value': '3a.m.'},
                         {'label': '04:00', 'value': '4a.m.'}, {'label': '05:00', 'value': '5a.m.'},
                         {'label': '06:00', 'value': '6a.m.'}, {'label': '07:00', 'value': '7a.m.'},
                         {'label': '08:00', 'value': '8a.m.'}, {'label': '09:00', 'value': '9a.m.'},
                         {'label': '10:00', 'value': '10a.m.'}, {'label': '11:00', 'value': '11a.m.'},
                         {'label': '12:00', 'value': '12p.m.'}, {'label': '13:00', 'value': '1p.m.'},
                         {'label': '14:00', 'value': '2p.m.'}, {'label': '15:00', 'value': '3p.m.'},
                         {'label': '16:00', 'value': '4p.m.'}, {'label': '17:00', 'value': '5p.m.'},
                         {'label': '18:00', 'value': '6p.m.'}, {'label': '19:00', 'value': '7p.m.'},
                         {'label': '20:00', 'value': '8p.m.'}, {'label': '21:00', 'value': '9p.m.'},
                         {'label': '22:00', 'value': '10p.m.'}, {'label': '23:00', 'value': '11p.m.'}],
                         style = {'width': '200px', 'margin':'20px'}),
        html.H3("Select road"),
        # Add a dropdown for the road
        dcc.Dropdown(id = "Road name",
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
                        style={'width':'150px','margin':'20px'}),
        html.H3("Here is the prediction for the road condition you have selected to see."),
        # need to insert their model here, then can output the result.
        ])
                         

if __name__ == '__main__':
    app.run_server(debug=True, port=8052)

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

image_folder="assets"
directory = os.fsencode(image_folder)
data = pd.read_csv("train_data.csv") 

app = dash.Dash(__name__)

app.layout = html.Div(
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
                      style = {'display': 'inline-block', 'width':'60px','margin':'20px'})
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
                html.H3('Density:', style={'font-weight': 'bold'}),
                html.H3('Speed:', style={'font-weight': 'bold'}),
                html.H3('Traffic condition:', style={'font-weight': 'bold'}),
                html.H3('Traffic condition:', style={'font-weight': 'bold'})
                ],
                style={'display':'none','padding':'20px','text-align': 'right'},
                id='attributes'
                )
            html.Div(
                children=[
                ],
                style = {'border': '1px solid black', 'width': '20%'}
            )],    
            style = {'display':'flex','align-items':'center','justify-content':'center'}
            ),


    #Data visualization
    html.Div(children = [
        html.Label(['Past data analysis'], style={'font-weight': 'bold'}),
        dcc.Dropdown(id='timeframe',
                        options=[
                            {'label':'last 30 minutes', 'value':'30'},
                            {'label':'last 1 hour', 'value':'60'}
                            ],
                     style = {'display': 'inline-block', 'width':'150px','margin':'20px'}),
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
@app.callback(
Output('camera_id','options'),
Input('road_name','value'))

def update_camera(road_name):
    df=data[data["express_way"]==road_name]
    return [{'label': i, 'value': str(i)} for i in df['camera_id'].unique()]
print(update_camera('KPE'))

#Enter camera id,date,time and timerange to find speed and density over time of past data
@app.callback(
[Output('img','children'),
 Output('attributes','style'),
 Output('speed','figure'),
Output('density','figure')],
[Input('camera_id','value'),
Input('traffic_date','date'),
Input('traffic_time','value'),
 Input('timeframe','value')])

def update_plot(camera_id,traffic_date,time,timeframe):
    #Stop update if missing values
    if traffic_date is not None:
        date_object = date.fromisoformat(traffic_date)
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
            img=[html.Img(src=image_folder+'/'+file)]
    # Plot graph by searching for images in past hr/half hr
    if timeframe:
        #Block update for now
        raise dash.exceptions.PreventUpdate
        variables=data.copy(deep=True)
        variables = variables.astype({'timestamp':'str','camera_id':'str'})
        variables['timestamp']=variables['timestamp'].str.slice(0,12)
        date_object = datetime.strptime(traffic_date, "%Y-%m-%d")
        time_object = datetime.strptime(time,'%H%M').time()  
        datetime_curr = datetime.combine(date_object, time_object)
        datetime_prev = datetime_curr - timedelta(hours=0, minutes=int(timeframe))
        datetime_curr = datetime.strftime(datetime_curr, "%Y%m%d%H%M")
        datetime_prev = datetime.strftime(datetime_prev, "%Y%m%d%H%M")
        variables = variables[variables['camera_id'] == camera_id ]
        variables = variables[variables['timestamp'] <= datetime_curr]
        variables = variables[variables['timestamp'] >= datetime_prev]
    #Placeholder values for graph
    speeddata = {'Time': ['11:00', '12:00', '13:00', '14:00','15:00'], 'Average_speed': [110, 100, 80, 55, 30]}
    densitydata = {'Time': ['11:00', '12:00', '13:00', '14:00','15:00'], 'Density': [0.8, 0.74, 0.66,0.55,0.43]}
    speedplot = px.line(speeddata, x='Time', y='Average_speed')
    densityplot = px.line(densitydata, x='Time', y='Density')
    return img,attributes_style,speedplot,densityplot
        #Intend to combine with past data
        #speedInput=
        #densityInput=
        #speedplot = px.line(graphInput, x='time', y='average_speed (km/h)')
        #densityplot = px.line(graphInput, x='time', y='density')
        #return speedplot,densityplot
    
if __name__ == '__main__':
    app.run_server(debug=True,port=8052)


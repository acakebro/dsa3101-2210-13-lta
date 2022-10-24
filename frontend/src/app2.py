import dash
import os
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from os import listdir
from dash.dependencies import Input, Output
from datetime import datetime, date,timedelta
from time import localtime, strftime
import dash_bootstrap_components as dbc

image_folder="assets"
directory = os.fsencode(image_folder)
data = pd.read_csv("train_data.csv")

app = dash.Dash(__name__)

app.layout = html.Div(
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
        html.H2('Past data analysis', style={'font-weight': 'bold'}),
        dcc.Dropdown(id='timeframe',
                        options=[
                            {'label':'last 30 minutes', 'value':'30'},
                            {'label':'last 1 hour', 'value':'60'}
                            ],
                     placeholder='last 15 minutes',
                     style = {'margin':'20px'}),
        dcc.Graph(
            id='speed',
            style = {'display': 'inline-block', 'width': '450px'}
        ),       
        dcc.Graph(
            id='density',
            style = {'display': 'inline-block', 'width': '450px'}
        )
        ],
        style = {'margin':'25px'}
        )
        ],
    style = {'background-color': 'rgb(237,250,252)'}
    )

@app.callback(
Output('camera_id','options'),
Input('road_name','value'))

def update_camera(road_name):
    df=data[data["express_way"]==road_name]
    return [{'label': i, 'value': str(i)} for i in df['camera_id'].unique()]

#Enter camera id,date,time and timerange to find speed and density over time of past data
@app.callback(
[Output('img','children'),
 Output('attributes','style'),
 Output('speed','figure'),
Output('density','figure'),
Output('datatable','children')],
[Input('camera_id','value'),
Input('traffic_date','date'),
Input('traffic_time','value'),
 Input('timeframe','value')])

def update_plot(camera_id,traffic_date,time,timeframe):
    #Stop update if missing values
    if traffic_date is not None:
        date_object = date.fromisoformat(traffic_date)
        date_time = date_object.strftime('%Y%m%d')
    if camera_id is None:
        camera_id='1001'
    if time is not None and len(str(time))!=4:
        raise dash.exceptions.PreventUpdate
    #Make hidden attributes appear
    attributes_style={'display':'inline-block','padding':'20px','text-align': 'right'}
    date_time+=str(time)
    #Search for image by datetime and camera_id
    for filename in os.listdir(directory):
        file = os.fsdecode(filename)
        if camera_id in file:
            img=[html.Img(src=image_folder+'/'+file,style={'height':'360px', 'width':'480px'})]
    if timeframe is None:
        timeframe=15
    archive=pd.read_csv("archive.csv")
    variables=archive.copy(deep=True)
    #Convert datetime into YYYYMMDDHHMM format
    variables['Date']=variables['Date'].str.slice(0,6)+'20'+variables['Date'].str.slice(6,)
    variables['Date']=variables['Date'].apply(lambda x: datetime.strptime(x, "%d/%m/%Y").strftime("%Y%m%d"))
    variables['Time']=variables['Time'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").strftime("%H%M"))
    variables['Time']=variables['Date']+variables['Time']
    variables.sort_values(["Camera_Id","Time"],axis=0, ascending=True,inplace=True,na_position='first')
    #Filter datetime within last timeframe(15 min,30min,1hr)
    datetime_curr= datetime(int(date_time[:4]),int(date_time[4:6]),int(date_time[6:8]),int(date_time[8:10]),int(date_time[10:]))
    datetime_prev = datetime_curr - timedelta(hours=0, minutes=int(timeframe))
    datetime_curr = datetime.strftime(datetime_curr, "%Y%m%d%H%M")
    datetime_prev = datetime.strftime(datetime_prev, "%Y%m%d%H%M")
    variables = variables[variables['Camera_Id'] == int(camera_id)]
    variables = variables[variables['Time'] <= datetime_curr]
    variables = variables[variables['Time'] >= datetime_prev]
    variables['Time']=variables['Time'].str.slice(8,10)+':'+variables['Time'].str.slice(10,12)
    # Plot graph by searching for values in last timeframe(15 min,30min,1hr)
    speedplot = px.line(variables, x='Time', y='Average_Speed',color="Direction",template='seaborn',title='Speed over time')
    densityplot = px.line(variables, x='Time', y='Density',color="Direction",template='seaborn',title='Density over time')

    #Load prediction data in table form
    variables=archive.copy(deep=True)
    variables['Date']=variables['Date'].str.slice(0,6)+'20'+variables['Date'].str.slice(6,)
    variables['Date']=variables['Date'].apply(lambda x: datetime.strptime(x, "%d/%m/%Y").strftime("%Y%m%d"))
    variables['Time']=variables['Time'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").strftime("%H%M"))
    variables['Time']=variables['Date']+variables['Time']
    datetime_curr= datetime(int(date_time[:4]),int(date_time[4:6]),int(date_time[6:8]),int(date_time[8:10]),int(date_time[10:]))
    datetime_prev = datetime_curr - timedelta(hours=0, minutes=5)
    datetime_curr = datetime.strftime(datetime_curr, "%Y%m%d%H%M")
    datetime_prev = datetime.strftime(datetime_prev, "%Y%m%d%H%M")
    variables = variables[variables['Time'] <= datetime_curr]
    variables = variables[variables['Time'] >= datetime_prev]
    variables = variables[variables['Camera_Id'] == int(camera_id)]
    variables = variables.loc[:,['Direction','Density','Average_Speed','Jam']]
    variables['Jam']=variables['Jam'].replace([1],'Jam')
    variables['Jam']=variables['Jam'].replace([0],'No Jam')
    variables=variables.T
    table=[dbc.Table.from_dataframe(variables, striped=True, bordered=True, hover=True,header=False,size='lg')]
    return img,attributes_style,speedplot,densityplot,table

    
if __name__ == '__main__':
    app.run_server(debug=True,port=8052)


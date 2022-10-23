from dash import dcc,html,dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash,os
import plotly.express as px
import pandas as pd
from datetime import datetime, date,timedelta

import pg1,pg2,pg3

from api_calls import ApiCall

api_obj = ApiCall("../interface")
api_obj.download_images()

image_folder="assets"
directory = os.fsencode(image_folder)
data = pd.read_csv("train_data.csv")

def Navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Overview", href="/page1")),
                dbc.NavItem(dbc.NavLink("Stats", href="/page2")),
                dbc.NavItem(dbc.NavLink("Predictions", href="/page3"))
            ] ,
            brand="Traffic App",
            brand_href="/page1",
            color="dark",
            dark=True,
        ), 
    ])

    return layout

nav = Navbar()

app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP], 
                meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav, 
    html.Div(id='page-content', children=[]), 
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))


def display_page(pathname):
    if pathname == '/page1':
         return pg1.layout
    elif pathname == '/page2':
         return pg2.layout
    elif pathname == '/page3':
         return pg3.layout
    return pg1.layout

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
    if camera_id is None:
        camera_id='1001'
    if time is not None and len(str(time))!=4:
        raise dash.exceptions.PreventUpdate
    #Make hidden attributes appear
    attributes_style={'display':'inline-block','padding':'20px','text-align': 'right'}
    datetime+=str(time)
    #Search for image by datetime and camera_id
    for filename in os.listdir(directory):
        file = os.fsdecode(filename)
        if camera_id in file:
            img=[html.Img(src=image_folder+'/'+file,style={'height':'360px', 'width':'480px'})]
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
    #Placeholder values for graph (last 4 hrs)
    speeddata = {'Time': ['16:45', '17:45', '18:45', '19:45','20:45'], 'Average_speed': [110, 100, 80, 55, 30]}
    densitydata = {'Time': ['16:45', '17:45', '18:45', '19:45','20:45'], 'Density': [0.8, 0.74, 0.66,0.55,0.43]}
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
    app.run_server(debug=True,port=8051)

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
archive = pd.read_csv("archive.csv")

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
    app.run_server(debug=True,port=8051)

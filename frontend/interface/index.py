from dash import dcc,html,dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash,os
import plotly.express as px
import pandas as pd
from datetime import datetime, date,timedelta
from flask import Flask
import requests
import csv

import pg1,pg2,pg3

from api_calls import ApiCall

#api_obj = ApiCall("../app")
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

def create_Img(link_list):

    img_list = [html.Div(children = [
        html.H2("ID: " + str(link_list[i][:4]),
                style = {'text-align': 'center',
                         'text-decoration': 'underline',
                         'margin': '50px 5px 1px 5px'}),
        html.Img(
        title = str(link_list[i][:4]),
        src= image_folder + "/" + link_list[i],
        style = {'display': 'inline-block', 'width': '420px', 'height': '250px',
                 'margin': '20px',
                 'border': '3px solid black'}),
        html.Br()],
                         style = {'display':'inline-block'}) for i in range(len(link_list))]
    return img_list

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

nav = Navbar()



server = Flask(__name__)

app = dash.Dash(__name__, server=server,
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
Output('datatable','children'),
Output('places','children')],
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
        if camera_id in file[:4]:
            img=[html.Img(src=image_folder+'/'+file,style={'height':'360px', 'width':'480px'})]
    if timeframe is None:
        timeframe=15

    #Pull prediction data from backend
    archive_json = requests.get('http://0.0.0.0:8050/archive?camera_id='+str(camera_id)).json()
    variables = pd.read_json(archive_json)
    #Convert datetime into YYYYMMDDHHMM format
    variables['Date']=variables['Date'].str.slice(0,6)+variables['Date'].str.slice(6,)
    variables['Date']=variables['Date'].apply(lambda x: datetime.strptime(x, "%d/%m/%Y").strftime("%Y%m%d"))
    variables['Time']=variables['Time'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").strftime("%H%M"))
    variables['Time']=variables['Date']+variables['Time']
    graph_inputs=variables.sort_values(["Camera_Id","Time"],axis=0, ascending=True,inplace=True,na_position='first')
    #Filter datetime within last timeframe(15 min,30min,1hr)
    datetime_curr= datetime(int(date_time[:4]),int(date_time[4:6]),int(date_time[6:8]),int(date_time[8:10]),int(date_time[10:]))
    datetime_prev = datetime_curr - timedelta(hours=0, minutes=int(timeframe))
    datetime_curr = datetime.strftime(datetime_curr, "%Y%m%d%H%M")
    datetime_prev = datetime.strftime(datetime_prev, "%Y%m%d%H%M")
    graph_inputs = graph_inputs[graph_inputs['Time'] <= datetime_curr]
    graph_inputs = graph_inputs[graph_inputs['Time'] >= datetime_prev]
    graph_inputs['Time']=graph_inputs['Time'].str.slice(8,10)+':'+graph_inputs['Time'].str.slice(10,12)
    # Plot graph by searching for values in last timeframe(15 min,30min,1hr)
    speedplot = px.line(graph_inputs, x='Time', y='Average_Speed',color="Direction",template='seaborn',title='Speed over time')
    densityplot = px.line(graph_inputs, x='Time', y='Density',color="Direction",template='seaborn',title='Density over time')

    #Load prediction data in table form
    #variables=archive.copy(deep=True)
    #variables['Date']=variables['Date'].str.slice(0,6)+variables['Date'].str.slice(6,)
    #variables['Date']=variables['Date'].apply(lambda x: datetime.strptime(x, "%d/%m/%Y").strftime("%Y%m%d"))
    #variables['Time']=variables['Time'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").strftime("%H%M"))
    #variables['Time']=variables['Date']+variables['Time']
    table=variables
    datetime_curr= datetime(int(date_time[:4]),int(date_time[4:6]),int(date_time[6:8]),int(date_time[8:10]),int(date_time[10:]))
    datetime_prev = datetime_curr - timedelta(hours=0, minutes=5)
    datetime_curr = datetime.strftime(datetime_curr, "%Y%m%d%H%M")
    datetime_prev = datetime.strftime(datetime_prev, "%Y%m%d%H%M")
    table = table[table['Time'] <= datetime_curr]
    table = table[table['Time'] >= datetime_prev]
    table = table.loc[:,['Direction','Density','Average_Speed','Jam']]
    table['Jam']=table['Jam'].replace([1],'Jam')
    table['Jam']=table['Jam'].replace([0],'No Jam')
    table=table.T
    datatable=[dbc.Table.from_dataframe(table, striped=True, bordered=True, hover=True,header=False)]

    #Table of congested areas
    variables=variables.assign(DateTime=variables['Time'])
    variables['DateTime']=variables['DateTime'].apply(lambda x:datetime(int(x[:4]),int(x[4:6]),int(x[6:8]),int(x[8:10]),int(x[10:])))
    datetime_curr= datetime(int(date_time[:4]),int(date_time[4:6]),int(date_time[6:8]),int(date_time[8:10]),int(date_time[10:]))
    datetime_prev = datetime_curr - timedelta(hours=0, minutes=30)
    datetime_range = datetime_curr - timedelta(hours=2, minutes=30)
    places={}
    with open("Image_ROI.csv") as file:
        read_file=csv.reader(file)
        next(read_file, None)
        for camera,roi,direction in read_file:
            areas=variables
            areas=areas[areas['Camera_Id']== int(camera)]
            areas=areas[areas['Direction']== direction]
            areas=areas[areas['DateTime']<= datetime_curr]
            areas=areas[areas['DateTime']>= datetime_range]
            temp=areas['DateTime']
            for time in temp:
                if time<=datetime_prev:
                    break
                time_range=areas[areas['DateTime']>= time - timedelta(hours=0, minutes=120)]
                if 0 in time_range['Jam']:
                    continue
                else:
                    realtime=time.strftime("%d%m%Y %H:%M")
                    if realtime not in places.keys():
                        places[realtime]=[]
                    places[realtime]+=[[camera,direction]]
    df = pd.DataFrame(data=places)
    places=[dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True,header=False,size='sm')]
    return img,attributes_style,speedplot,densityplot,datatable,places

@app.callback(
    Output(component_id='img_out', component_property='children'),
    Input(component_id='exp_dd', component_property='value'),
    #Input(component_id='reg_dd', component_property='value')
)


def filter_image(input_exp):
    image_path = os.listdir(image_folder)
    if input_exp != 'All':
        exp_filter = input_exp
        camid = d_exp_cam[exp_filter]
        filtered_image_path = []
        for i in image_path:
            if i[:4] in camid:
                filtered_image_path.append(i)
        return create_Img(filtered_image_path)
    return create_Img(image_path)





if __name__ == '__main__':
    #app.run_server(host='0.0.0.0',debug=True, port=8050)
    app.run_server(debug=True, port = 8051)

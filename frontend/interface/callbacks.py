from maindash import app
from dash import dcc,html,dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from pandas import json_normalize 
import dash,os
import plotly.express as px
import pandas as pd
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import assign
from datetime import datetime, date,timedelta
from flask import Flask, jsonify, request, send_file
from glob import glob
import requests
import pg1,pg2,pg3
import csv
from time import strftime,localtime

image_folder="assets"
directory = os.fsencode(image_folder)
data = pd.read_csv("train_data.csv")

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



image_folder="assets"


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

chroma = "https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"  # js lib used for colors


point_to_layer = assign("""function(feature, latlng, context){
    const {min, max, colorscale, circleOptions, colorProp} = context.props.hideout;
    const csc = chroma.scale(colorscale).domain([min, max]);  // chroma lib to construct colorscale
    circleOptions.fillColor = csc(feature.properties[colorProp]);  // set color based on color prop.
    return L.circleMarker(latlng, circleOptions);  // sender a simple circle marker.
    }""")


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
    if road_name is None:
        road_name='KPE'
    return [{'label': i, 'value': str(i)} for i in d_exp_cam[str(road_name)]]

#Enter camera id,date,time and timerange to find speed and density over time of past data
@app.callback(
[Output('img','children'),
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
    if time is None:
        time=strftime("%H%M", localtime()),
    if time is not None and len(str(time))!=4:
        raise dash.exceptions.PreventUpdate
    #Make hidden attributes appear
    date_time+=str(time)
    print(date_time)
    #Search for image by datetime and camera_id
    for filename in os.listdir(directory):
        file = os.fsdecode(filename)
        if camera_id in file[:5]:
            img=[html.Img(src=image_folder+'/'+file,style={'height':'360px', 'width':'480px'})]
    if timeframe is None:
        timeframe=60

    #Pull prediction data from backend
    stats_json = requests.get('http://127.0.0.1:9001/stats?camera_id='+str(camera_id)).json()
    variables = json_normalize(stats_json)
    #Convert datetime into YYYYMMDDHHMM format
    variables['Date']=variables['Date'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").strftime("%Y%m%d"))
    variables['Time']=variables['Time'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").strftime("%H%M"))
    variables['Time']=variables['Date']+variables['Time']
    variables.sort_values(["Time"],axis=0, ascending=False,inplace=True,na_position='first')
    datetime_curr= datetime(int(date_time[:4]),int(date_time[4:6]),int(date_time[6:8]),int(date_time[8:10]),int(date_time[10:]))
    datetime_curr = datetime.strftime(datetime_curr, "%Y%m%d%H%M")
    variables = variables[variables['Time'] <= datetime_curr]
    graph_inputs=variables
    table=variables

    #Filter datetime within last timeframe(15 min,30min,1hr)
    temp=graph_inputs.loc[0,'Time']
    datetime_curr = datetime(int(temp[:4]),int(temp[4:6]),
                int(temp[6:8]),int(temp[8:10]),int(temp[10:]))
    datetime_prev = datetime_curr - timedelta(hours=0, minutes=int(timeframe))
    datetime_curr = datetime.strftime(datetime_curr, "%Y%m%d%H%M")    
    datetime_prev = datetime.strftime(datetime_prev, "%Y%m%d%H%M")
    graph_inputs = graph_inputs[graph_inputs['Time'] >= datetime_prev]
    graph_inputs['Time']=graph_inputs['Time'].str.slice(8,10)+':'+graph_inputs['Time'].str.slice(10,12)
    # Plot graph by searching for values in last timeframe(1hr,2hr,3hr)
    speedplot = px.line(graph_inputs, x='Time', y='Average_Speed',color="Direction",template='seaborn',title='Speed over time')
    densityplot = px.line(graph_inputs, x='Time', y='Density',color="Direction",template='seaborn',title='Density over time')

    #Load prediction data in table form
    table = table[table['Time'] == table.loc[0,'Time']]
    table = table.loc[:,['Direction','Density','Average_Speed','Jam']]
    table['Jam']=table['Jam'].replace([1],'Jam')
    table['Jam']=table['Jam'].replace([0],'No Jam')
    table=table.T
    datatable=[dbc.Table.from_dataframe(table, striped=True, bordered=True, hover=True,header=False)]

    #Table of congested areas
    archive_json = requests.get('http://127.0.0.1:9001/archive').json()
    variables = json_normalize(archive_json)
    variables['Date']=variables['Date'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").strftime("%Y%m%d"))
    variables['Time']=variables['Time'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").strftime("%H%M"))
    variables['Time']=variables['Date']+variables['Time']
    variables=variables.assign(DateTime=variables['Time'])
    variables['DateTime']=variables['DateTime'].apply(lambda x:datetime(int(x[:4]),int(x[4:6]),
                                                                    int(x[6:8]),int(x[8:10]),int(x[10:])))
    variables.sort_values(["Camera_Id","Time"],axis=0, ascending=False,inplace=True,na_position='first')
    datetime_curr= datetime(int(date_time[:4]),int(date_time[4:6]),int(date_time[6:8]),int(date_time[8:10]),int(date_time[10:]))
    datetime_curr = datetime.strftime(datetime_curr, "%Y%m%d%H%M")
    variables = variables[variables['Time'] <= datetime_curr]

    datetime_curr= variables.loc[0,'DateTime']
    datetime_prev = datetime_curr - timedelta(hours=0, minutes=30)
    datetime_range = datetime_curr - timedelta(hours=3, minutes=0)
    places={}
    with open("Image_ROI.csv") as file:
        read_file=csv.reader(file)
        next(read_file, None)
        for camera,roi,direction in read_file:
            areas=variables
            areas=areas[areas['Camera_Id']== str(camera)]
            areas=areas[areas['Direction']== direction]
            areas=areas[areas['DateTime']>= datetime_range]
            temp=areas['DateTime']
            for time in temp:
                if time<=datetime_prev:
                    break
                time_range=areas[areas['Time']>= time - timedelta(hours=0, minutes=150)]
                if len(time_range[time_range['Jam']== 0])!=0 or len(time_range[time_range['DateTime']<=time - timedelta(hours=0, minutes=120)])==0:
                    continue
                else:
                    realtime=time.strftime("%d/%m %H:%M")
                    if realtime not in places.keys():
                        places[realtime]=[]
                    places[realtime]+=[(camera,direction)]
    df = pd.DataFrame(data=places)
    places=[dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True,header=False,size='sm')]
    return img,speedplot,densityplot,datatable,places

@app.callback(
    Output(component_id='img_out', component_property='children'),
    Input(component_id='exp_dd', component_property='value'),
)


def filter_image(input_exp):
    image_path = list(filter(lambda x: "jpg" in x, os.listdir(image_folder)))
    if input_exp != 'All':
        exp_filter = input_exp
        camid = d_exp_cam[exp_filter]
        filtered_image_path = []
        for i in image_path:
            if i[:4] in camid:
                filtered_image_path.append(i)
        return create_Img(filtered_image_path)
    return create_Img(image_path)

@app.callback(
    Output(component_id = 'aggregation', component_property = 'options'),
    Input(component_id = 'attribute', component_property = 'value'),
    )

def update_dd(attr):
    all_agg = ["Max", "Min", "Average"]
    if attr == "Speed":
        return [{'label': "Average", 'value': "Average"}]

    return [{'label': x, 'value': x} for x in all_agg]

@app.callback(
    Output(component_id = 'aggregation', component_property = 'value'),
    Input(component_id = 'attribute', component_property = 'value'),
    )

def auto_select_avg(attr):
    if attr == "Speed":
        return "Average"
    else:
        return "Max"


@app.callback(
    Output(component_id = 'variable', component_property = 'children'),
    Input(component_id = 'attribute', component_property = 'value'),
    Input(component_id = 'aggregation', component_property = 'value')
    )

def update_map(input_attr, input_agg):
    # reading in the generated traffic_stats 
    df_json = requests.get('http://127.0.0.1:9001/archive').json()
    df = json_normalize(df_json)
    # df = pd.read_csv('training_data.csv')
    df['Date']=pd.to_datetime(df['Date'])
    df['Time']=df['Time'].replace(':','', regex=True)
    df['Time'] = df['Time'].str[:2]
    df['Time'] = df['Time'].apply(pd.to_numeric,errors='coerce')
    df1 = df[df['Date']==df['Date'].max()]
    df2 = df1[df1['Time']==df1['Time'].max()]
    
    color_prop0 = 'Density'
    colorscale0 = ['green','yellow','orange','red']
    if input_attr == 'Density':
        if input_agg == "Max":
            df0 = df2.sort_values('Density', ascending = False).drop_duplicates(subset='Camera_Id').sort_index()
            df0= df0[['Latitude', 'Longitude', 'Direction', 'Camera_Id', 'Jam',color_prop0, 'Vehicle_Count','Incident','Time']]
            dicts0 = df0.to_dict('records')
            for item in dicts0:
                if item['Jam']==1:
                    if item['Incident']==1:
                        item["tooltip"] = 'Camera {} <br/>Traffic density along {}: {:.2f} <br/>Vehicle Count: {} <br/>Jam: Yes <br/>Incident nearby (200m): Yes'.format(item['Camera_Id'], item['Direction'], item[color_prop0], item['Vehicle_Count']) # bind tooltip max
                    else:
                        item["tooltip"] = 'Camera {} <br/>Traffic density along {}: {:.2f} <br/>Vehicle Count: {} <br/>Jam: Yes <br/>Incident nearby (200m): No'.format(item['Camera_Id'], item['Direction'], item[color_prop0], item['Vehicle_Count']) # bind tooltip max   
                else:
                    if item['Incident']==1:
                        item["tooltip"] = 'Camera {} <br/>Traffic density along {}: {:.2f} <br/>Vehicle Count: {} <br/>Jam: No <br/>Incident nearby (200m): Yes'.format(item['Camera_Id'], item['Direction'], item[color_prop0], item['Vehicle_Count']) # bind tooltip max
                    else:
                        item["tooltip"] = 'Camera {} <br/>Traffic density along {}: {:.2f} <br/>Vehicle Count: {} <br/>Jam: No <br/>Incident nearby (200m): No'.format(item['Camera_Id'], item['Direction'], item[color_prop0], item['Vehicle_Count']) # bind tooltip max
        elif input_agg == 'Min':
             df0 = df2.sort_values('Density', ascending = True).drop_duplicates(subset='Camera_Id').sort_index()
             df0= df0[['Latitude', 'Longitude', 'Direction', 'Camera_Id', 'Jam',color_prop0, 'Vehicle_Count','Incident','Time']]
             dicts0 = df0.to_dict('records')
             for item in dicts0:
                 if item['Jam']==1:
                     if item['Incident']==1:
                         item["tooltip"] = 'Camera {} <br/>Traffic density along {}: {:.2f} <br/>Vehicle Count: {} <br/>Jam: Yes <br/>Incident nearby (200m): Yes'.format(item['Camera_Id'], item['Direction'], item[color_prop0], item['Vehicle_Count']) # bind tooltip max
                     else:
                         item["tooltip"] = 'Camera {} <br/>Traffic density along {}: {:.2f} <br/>Vehicle Count: {} <br/>Jam: Yes <br/>Incident nearby (200m): No'.format(item['Camera_Id'], item['Direction'], item[color_prop0], item['Vehicle_Count']) # bind tooltip max   
                 else:
                     if item['Incident']==1:
                         item["tooltip"] = 'Camera {} <br/>Traffic density along {}: {:.2f} <br/>Vehicle Count: {} <br/>Jam: No <br/>Incident nearby (200m): Yes'.format(item['Camera_Id'], item['Direction'], item[color_prop0], item['Vehicle_Count']) # bind tooltip max
                     else:
                         item["tooltip"] = 'Camera {} <br/>Traffic density along {}: {:.2f} <br/>Vehicle Count: {} <br/>Jam: No <br/>Incident nearby (200m): No'.format(item['Camera_Id'], item['Direction'], item[color_prop0], item['Vehicle_Count']) # bind tooltip max
        
        else: # Average
             df0 = df2.groupby(['Camera_Id', 'Longitude','Latitude', 'Incident','Time'])['Density'].mean().reset_index()
             df0= df0[['Latitude', 'Longitude', 'Camera_Id', color_prop0, 'Incident','Time']]
             dicts0 = df0.to_dict('records')
             for item in dicts0:
                 if item['Incident']==1:
                     item["tooltip"] = 'Camera {} <br/>Average traffic density: {:.2f} <br/>Incident nearby (200m): Yes'.format(item['Camera_Id'], item[color_prop0]) # bind tooltip max
                 else:
                     item["tooltip"] = 'Camera {} <br/>Average traffic density: {:.2f} <br/>Incident nearby (200m): No'.format(item['Camera_Id'], item[color_prop0])

    else:       # Average Speed
        if input_agg == "Average":
            df0 = df2.sort_values('Average_Speed', ascending = False).drop_duplicates(subset='Camera_Id').sort_index()
            colorscale0 = ['green','yellow','orange','red'] 
            color_prop0 = 'Average_Speed'
            dicts0 = df0.to_dict('records')
            for item in dicts0:
                if item['Jam']==1:
                    if item['Incident']==1:
                        item["tooltip"] = 'Camera {} <br/>Average speed along all lanes: {:.2f} <br/>Vehicle Count: {} <br/>Jam: Yes <br/>Incident nearby (200m): Yes'.format(item['Camera_Id'], item[color_prop0], item['Vehicle_Count'])
                    else:
                        item["tooltip"] = 'Camera {} <br/>Average speed along all lanes: {:.2f} <br/>Vehicle Count: {} <br/>Jam: Yes <br/>Incident nearby (200m): No'.format(item['Camera_Id'], item[color_prop0], item['Vehicle_Count'])
                else:
                    if item['Incident']==1:
                        item["tooltip"] = 'Camera {} <br/>Average speed along all lanes: {:.2f} <br/>Vehicle Count: {} <br/>Jam: No <br/>Incident nearby (200m): Yes'.format(item['Camera_Id'], item[color_prop0], item['Vehicle_Count'])
                    else:
                        item["tooltip"] = 'Camera {} <br/>Average speed along all lanes: {:.2f} <br/>Vehicle Count: {} <br/>Jam: No <br/>Incident nearby (200m): No'.format(item['Camera_Id'], item[color_prop0], item['Vehicle_Count'])

        else:
           return default_map


    geojson0 = dlx.dicts_to_geojson(dicts0, lon="Longitude", lat="Latitude")
    geobuf0 = dlx.geojson_to_geobuf(geojson0)
    vmax0 = df0[color_prop0].max()
    if input_attr == 'Density':
        colorbar0 = dl.Colorbar(colorscale=colorscale0, width=20, height=150, min=0, max=vmax0, unit='density per lane', opacity=0.9)
    else:
        colorbar0 = dl.Colorbar(colorscale=colorscale0, width=20, height=150, min=0, max=vmax0, unit='km/h', opacity=0.9)
    geojson0 = dl.GeoJSON(data=geobuf0, id="geojson", format="geobuf",
                    zoomToBounds=True,  # when true, zooms to bounds when data changes
                    options=dict(pointToLayer=point_to_layer),  # how to draw points
                    superClusterOptions=dict(radius=50),   # adjust cluster size
                    hideout=dict(colorProp=color_prop0, circleOptions=dict(fillOpacity=0.8, stroke=False, radius=7),
                              min=0, max=vmax0, colorscale=colorscale0))
    fullmap = dl.Map([dl.TileLayer(url='https://maps-{s}.onemap.sg/v3/Grey/{z}/{x}/{y}.png', maxZoom=13, minZoom=12,
                             attribution='<img src="https://www.onemap.gov.sg/docs/maps/images/oneMap64-01.png" style="height:20px;width:20px;"/> OneMap | Map data &copy; contributors, <a href="http://SLA.gov.sg">Singapore Land Authority</a>'),
    geojson0, colorbar0], center=[1.3521, 103.8198],
                          style={'width': '90%', 'height': '80vh', 'margin': "auto", "display": "block", "position": "relative"},)


    return fullmap

@app.callback(
Output('predict','value'),
[Input('traffic_time','value'),
 Input('traffic_date','date'),
 Input('camera_id','value'),
 Input('road_name','value')])

def update_prediction(camera_id,road,traffic_date,time):
    
    if traffic_date is None:
        traffic_date = date.today().strftime('%d/%m/%Y')
    if road is None:
        road='KPE'
    if camera_id is None:
        camera_id='1001'
    if time is None:
        time = datetime.now().strftime("%H:%M")
    if time is not None and len(str(time))!=4:
        raise dash.exceptions.PreventUpdate
    stats = requests.get('http://127.0.0.1:9001/prediction?camera_id='+str(camera_id)+'&date='+str(traffic_date)+'&time='+str(time)+'&road='+str(road)).json()['prediction']
    return stats


from maindash import app
from dash import dcc,html,dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
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


df = pd.read_csv("training_data.csv")
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
        if camera_id in file[:5]:
            img=[html.Img(src=image_folder+'/'+file,style={'height':'360px', 'width':'480px'})]
    if timeframe is None:
        timeframe=15

    #Pull prediction data from backend
    speeddata = {'Time': ['16:45', '17:45', '18:45','16:45', '17:45', '18:45','16:45', '17:45', '18:45'],
                 'Average_Speed': [110, 100, 80, 55,30,90,70,48,56],
                 'Direction':['WOODLANDS','WOODLANDS','WOODLANDS','PIE JURONG','PIE JURONG','PIE JURONG','PIE CHANGI','PIE CHANGI','PIE CHANGI']}
    densitydata = {'Time': ['16:45', '17:45', '18:45','16:45', '17:45', '18:45','16:45', '17:45', '18:45'],
                   'Density': [0.8, 0.74, 0.66,0.55,0.43,0.70,0.58,0.50,0.55],
                   'Direction':['WOODLANDS','WOODLANDS','WOODLANDS','PIE JURONG','PIE JURONG','PIE JURONG','PIE CHANGI','PIE CHANGI','PIE CHANGI']}
    speedplot = px.line(speeddata, x='Time', y='Average_Speed',color="Direction",template='seaborn',title='Speed over time')
    densityplot = px.line(densitydata, x='Time', y='Density',color="Direction",template='seaborn',title='Density over time')

    #Load prediction data in table form
    table={'Direction':['WOODLANDS','PIE JURONG','PIE CHANGI'],'Density':[0.07,0,0.07],'Speed':[100,100,100],'Traffic condition':['No Jam','No Jam','No Jam']}
    table=pd.DataFrame.from_dict(table)
    table=table.T
    datatable=[dbc.Table.from_dataframe(table, striped=True, bordered=True, hover=True,header=False)]

    #Table of congested areas
    df = {'Areas':['30/10/2022 6:34pm (1001,WOODLANDS),(9702,TPE)','30/10/2022 5:06pm (1505,MCE(ECP))']}
    df=pd.DataFrame.from_dict(df)
    places=[dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True,header=False,size='sm')]
    return img,attributes_style,speedplot,densityplot,datatable,places

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
    color_prop0 = 'Density'
    colorscale0 = ['green','yellow','orange','red']
    if input_attr == 'Density':
        if input_agg == "Max":
            df0 = df.sort_values('Density', ascending = False).drop_duplicates(subset='Camera_Id').sort_index()
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
             df0 = df.sort_values('Density', ascending = True).drop_duplicates(subset='Camera_Id').sort_index()
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
             df0 = df.groupby(['Camera_Id', 'Longitude','Latitude', 'Incident','Time'])['Density'].mean().reset_index()
             df0= df0[['Latitude', 'Longitude', 'Camera_Id', color_prop0, 'Incident','Time']]
             dicts0 = df0.to_dict('records')
             for item in dicts0:
                 if item['Incident']==1:
                     item["tooltip"] = 'Camera {} <br/>Average traffic density: {:.2f} <br/>Incident nearby (200m): Yes'.format(item['Camera_Id'], item[color_prop0]) # bind tooltip max
                 else:
                     item["tooltip"] = 'Camera {} <br/>Average traffic density: {:.2f} <br/>Incident nearby (200m): No'.format(item['Camera_Id'], item[color_prop0])

    else:       # Average Speed
        if input_agg == "Average":
            df0 = df.sort_values('Average_Speed', ascending = False).drop_duplicates(subset='Camera_Id').sort_index()
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
    vmax0 = df[color_prop0].max()
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

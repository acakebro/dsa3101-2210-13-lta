'''
 # @ Create Time: 2022-10-08 23:39:32.168931
'''

import sys
import pathlib

sys.path.insert(1, "../../backend/Model/")


from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
import sys
from api_calls import ApiCall
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from datetime import datetime, date
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import assign
import os
from api_calls import ApiCall


#api_obj = ApiCall("../src")
#api_obj.download_images()

chroma = "https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"  # js lib used for colors

app = Dash(__name__, external_scripts = [chroma], title="frontend")

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

traffic_incidents = pd.read_csv("traffic_incidents.csv")
traffic_speedbands = pd.read_csv("traffic_speedbands.csv")
traffic_images = pd.read_csv("traffic_images.csv")
df = pd.read_csv("../../backend/Model/training_data.csv")

default_map = dl.Map([dl.TileLayer(url='https://maps-{s}.onemap.sg/v3/Grey/{z}/{x}/{y}.png', maxZoom=13, minZoom=12,

                             attribution='< img src="https://www.onemap.gov.sg/docs/maps/images/oneMap64-01.png" style="height:20px;width:20px;"/> OneMap | Map data &copy; contributors, <a href=" ">Singapore Land Authority</a >'),
    ], center=[1.3521, 103.8198],
                          style={'width': '90%', 'height': '80vh', 'margin': "auto", "display": "block", "position": "relative"},)


folder = "assets/"

date_time = traffic_incidents['Message'].str.split(" ", 1, expand = True).iloc[:,0]
message = traffic_incidents['Message'].str.split(" ", 1, expand = True).iloc[:,1]
time = date_time.str.split(")", expand = True).iloc[:,1]
date = date_time.str.split(")", expand = True).iloc[:,0].str[1:]
traffic_incidents_new = traffic_incidents.drop("Message", axis = 1)
traffic_incidents_new['Date'] = date
traffic_incidents_new['Time'] = time
traffic_incidents_new['Message'] = message

point_to_layer = assign("""function(feature, latlng, context){
    const {min, max, colorscale, circleOptions, colorProp} = context.props.hideout;
    const csc = chroma.scale(colorscale).domain([min, max]);  // chroma lib to construct colorscale
    circleOptions.fillColor = csc(feature.properties[colorProp]);  // set color based on color prop.
    return L.circleMarker(latlng, circleOptions);  // sender a simple circle marker.
    }""")

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

d_reg_cam = ''

def create_Img(link_list):

    img_list = [html.Div(children = [
        html.H2("ID: " + str(link_list[i][:4]),
                style = {'text-align': 'center',
                         'text-decoration': 'underline',
                         'margin': '50px 5px 1px 5px'}),
        html.Img(
        title = str(link_list[i][:4]),
        src= folder + link_list[i],
        style = {'display': 'inline-block', 'width': '420px', 'height': '250px',
                 'margin': '20px',
                 'border': '3px solid black'}),
        html.Br()],
                         style = {'display':'inline-block'}) for i in range(len(link_list))]
    return img_list



d_table_in = dash_table.DataTable(
            data=traffic_incidents_new.iloc[:5,:].to_dict('records'),
            columns = [{"name": ["Traffic Incidents", i], "id": i} for i in traffic_incidents_new.columns[-3:]],
            cell_selectable=False,
            sort_action='native',
            #filter_action= False,
            page_action = 'native',
            page_current = 0,
            page_size = 10,
            style_as_list_view = True,
            style_cell_conditional = [
                {'if':{'column_id': 'Date'},
                 'text-align': 'center'},
                {'if':{'column_id': 'Time'},
                 'text-align': 'center'}
                ],
            style_cell = {'padding': '5px',
                          'width': '150px',
                          'font_family': 'Tahoma'},
            style_header = {
                'text-align': 'center',
                'backgroundColor': 'lightgrey',
                'fontWeight': 'bold',
                'fontSize': '18px'},
            merge_duplicate_headers = True
            )


app.layout = html.Div(children=[
    html.H1(children='Title', style = {'text-align':'center'}),

    # map
    html.Div(
        children=[
            html.H4('Select Attribute', style={'font-weight': 'bold'}),
            # Add a dropdown with identifier
            dcc.Dropdown(id = 'attribute',
            options=[
                {'label':'Density', 'value': 'Density'},
                {'label':'Speed', 'value': 'Speed'},],
                         value = 'Density',
                style={'width':'120px', 'margin':'0 auto', 'display': 'inline-block'}
                         ),
            html.H4('Select Aggregation', style={'font-weight': 'bold'}),
            # Add a dropdown with identifier
            dcc.Dropdown(id = 'aggregation',
            options=[
                {'label':'Max', 'value': 'Max'},
                {'label':'Min', 'value': 'Min'},
                {'label':'Average', 'value': 'Average'},],
                         value = 'Max',
                style={'width':'120px', 'margin':'0 auto', 'display': 'inline-block'}
                         )],
            style={'width':'45%', 'vertical-align':'top',
                   'padding':'20px', 'margin':'0 auto', 'display':'flex','align-items': 'center', 'justify-content':'center'}
        ),
    
    html.Div(id = 'variable',
        style = {'width':'90%', 'height':'80vh', 'margin':'0 auto', 'position':'relative'}
             ),
    
    html.Br(),
    html.Br(),

    # filter box
    html.Div(children = [

    html.H4("Select Direction", style={'font-weight': 'bold'}),
    dcc.Dropdown(id = "exp_dd",
                 options = [
            {'label': 'All' + " (" + str(len(list(filter(lambda x: "jpg" in x, os.listdir(folder))))) + ")", 'value': 'All'},
            {'label':'KPE' + " (" + str(len(d_exp_cam['KPE'])) + ")", 'value':'KPE'},
            {'label':'ECP' + " (" + str(len(d_exp_cam['ECP'])) + ")", 'value':'ECP'},
            {'label':'KJE' + " (" + str(len(d_exp_cam['KJE'])) + ")", 'value':'KJE'},
            {'label':'SLE' + " (" + str(len(d_exp_cam['SLE'])) + ")", 'value':'SLE'},
            {'label':'MCE' + " (" + str(len(d_exp_cam['MCE'])) + ")", 'value':'MCE'},
            {'label':'CTE' + " (" + str(len(d_exp_cam['CTE'])) + ")", 'value':'CTE'},
            {'label':'TPE' + " (" + str(len(d_exp_cam['TPE'])) + ")", 'value':'TPE'},
            {'label':'BKE' + " (" + str(len(d_exp_cam['BKE'])) + ")", 'value':'BKE'},
            {'label':'PIE' + " (" + str(len(d_exp_cam['PIE'])) + ")", 'value':'PIE'},
            {'label':'AYE' + " (" + str(len(d_exp_cam['AYE'])) + ")", 'value':'AYE'},
            {'label':'Woodlands Causeway/Johor' + " (" + str(len(d_exp_cam['Woodlands Causeway/Johor'])) + ")", 'value':'Woodlands Causeway/Johor'},
            {'label':'Tuas/Johor' + " (" + str(len(d_exp_cam['Tuas/Johor'])) + ")", 'value':'Tuas/Johor'},
            {'label':'Changi' + " (" + str(len(d_exp_cam['Changi'])) + ")", 'value':'Changi'},
            {'label':'City' + " (" + str(len(d_exp_cam['City'])) + ")", 'value':'City'},
            {'label':'Moulmein' + " (" + str(len(d_exp_cam['Moulmein'])) + ")", 'value':'Moulmein'},
            {'label':'Yio Chu Kang' + " (" + str(len(d_exp_cam['Yio Chu Kang'])) + ")", 'value':'Yio Chu Kang'},
            {'label':'Jalan Bukit Merah' + " (" + str(len(d_exp_cam['Jalan Bukit Merah'])) + ")", 'value':'Jalan Bukit Merah'},
            {'label':'Jurong' + " (" + str(len(d_exp_cam['Jurong'])) + ")", 'value':'Jurong'},
            {'label':'Airport' + " (" + str(len(d_exp_cam['Airport'])) + ")", 'value':'Airport'},
            {'label':'Xilin Ave' + " (" + str(len(d_exp_cam['Xilin Ave'])) + ")", 'value':'Xilin Ave'},
            {'label':'Marine Parade' + " (" + str(len(d_exp_cam['Marine Parade'])) + ")", 'value':'Marine Parade'},
            {'label':'Telok Blangah' + " (" + str(len(d_exp_cam['Telok Blangah'])) + ")", 'value':'Telok Blangah'},
            {'label':'Sentosa' + " (" + str(len(d_exp_cam['Sentosa'])) + ")", 'value':'Sentosa'},
            {'label':'Toa Payoh' + " (" + str(len(d_exp_cam['Toa Payoh'])) + ")", 'value':'Toa Payoh'},
            {'label':'Thomson' + " (" + str(len(d_exp_cam['Thomson'])) + ")", 'value':'Thomson'},
            {'label':'Pasir Ris Dr 12' + " (" + str(len(d_exp_cam['Pasir Ris Dr 12'])) + ")", 'value':'Pasir Ris Dr 12'},
            {'label':'Punggol/Sengkang' + " (" + str(len(d_exp_cam['Punggol/Sengkang'])) + ")", 'value':'Punggol/Sengkang'},
            {'label':'Choa Chu Kang' + " (" + str(len(d_exp_cam['Choa Chu Kang'])) + ")", 'value':'Choa Chu Kang'},
            {'label':'Woodlands Ave 2' + " (" + str(len(d_exp_cam['Woodlands Ave 2'])) + ")", 'value':'Woodlands Ave 2'}],
                 value = 'All',
                 style = {'display': 'inline-block', 'width':'170px','margin': '0 auto', 'cursor': 'pointer',
                          'border-radius': '5px'})
    ], style = {'width': '25%', 'display': 'inline-block','text-align': 'center', 'border-radius':'5px',
                'padding':'20px', 'margin':'0 auto', 'display':'flex','align-items': 'center', 'justify-content':'center'},
             ),

    # table
    html.Div([
        html.Table(children = [d_table_in])],
               style = {'display': 'inline-block', 'margin-left': '150px'}),


    # time
    html.Div([
        html.Br(),
        html.H4("Time: " + datetime.now().strftime("%d/%m/%Y  %I:%M %p"),
                style = {'text-align': 'right',
                         'margin': '10px'})]),

    # images
    #html.Div(children = [
    #*create_Img(os.listdir(folder))],
    #         style = {'text-align':'center', 'font-size':18}
    #         )
    html.Div(id = "img_out", style = {'text-align':'center', 'font-size':18})
    

    ],
                      style = {'background-color': 'white'}
                      )


@app.callback(
    Output(component_id='img_out', component_property='children'),
    Input(component_id='exp_dd', component_property='value'),
)


def filter_image(input_exp):
    image_path = list(filter(lambda x: "jpg" in x, os.listdir(folder)))
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
            df0= df0[['Latitude', 'Longitude', 'Direction', 'Camera_Id', 'Jam',color_prop0, 'Incident','Time']]
            dicts0 = df0.to_dict('records')
            for item in dicts0:
                if item['Jam']==1:
                    if item['Incident']==1:
                        item["tooltip"] = 'Camera {} <br/>Traffic density along {}: {:.2f} <br/>Jam: Yes <br/>Incident nearby (200m): Yes'.format(item['Camera_Id'], item['Direction'], item[color_prop0]) # bind tooltip max
                    else:
                        item["tooltip"] = 'Camera {} <br/>Traffic density along {}: {:.2f} <br/>Jam: Yes <br/>Incident nearby (200m): No'.format(item['Camera_Id'], item['Direction'], item[color_prop0]) # bind tooltip max   
                else:
                    if item['Incident']==1:
                        item["tooltip"] = 'Camera {} <br/>Traffic density along {}: {:.2f} <br/>Jam: No <br/>Incident nearby (200m): Yes'.format(item['Camera_Id'], item['Direction'], item[color_prop0]) # bind tooltip max
                    else:
                        item["tooltip"] = 'Camera {} <br/>Traffic density along {}: {:.2f} <br/>Jam: No <br/>Incident nearby (200m): No'.format(item['Camera_Id'], item['Direction'], item[color_prop0]) # bind tooltip max
        elif input_agg == 'Min':
             df0 = df.sort_values('Density', ascending = True).drop_duplicates(subset='Camera_Id').sort_index()
             df0= df0[['Latitude', 'Longitude', 'Direction', 'Camera_Id', 'Jam',color_prop0, 'Incident','Time']]
             dicts0 = df0.to_dict('records')
             for item in dicts0:
                 if item['Jam']==1:
                     if item['Incident']==1:
                         item["tooltip"] = 'Camera {} <br/>Traffic density along {}: {:.2f} <br/>Jam: Yes <br/>Incident nearby (200m): Yes'.format(item['Camera_Id'], item['Direction'], item[color_prop0]) # bind tooltip max
                     else:
                         item["tooltip"] = 'Camera {} <br/>Traffic density along {}: {:.2f} <br/>Jam: Yes <br/>Incident nearby (200m): No'.format(item['Camera_Id'], item['Direction'], item[color_prop0]) # bind tooltip max   
                 else:
                     if item['Incident']==1:
                         item["tooltip"] = 'Camera {} <br/>Traffic density along {}: {:.2f} <br/>Jam: No <br/>Incident nearby (200m): Yes'.format(item['Camera_Id'], item['Direction'], item[color_prop0]) # bind tooltip max
                     else:
                         item["tooltip"] = 'Camera {} <br/>Traffic density along {}: {:.2f} <br/>Jam: No <br/>Incident nearby (200m): No'.format(item['Camera_Id'], item['Direction'], item[color_prop0]) # bind tooltip max
        
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
                        item["tooltip"] = 'Camera {} <br/>Average speed along all lanes: {:.2f} <br/>Jam: Yes <br/>Incident nearby (200m): Yes'.format(item['Camera_Id'], item[color_prop0])
                    else:
                        item["tooltip"] = 'Camera {} <br/>Average speed along all lanes: {:.2f} <br/>Jam: Yes <br/>Incident nearby (200m): No'.format(item['Camera_Id'], item[color_prop0])
                else:
                    if item['Incident']==1:
                        item["tooltip"] = 'Camera {} <br/>Average speed along all lanes: {:.2f} <br/>Jam: No <br/>Incident nearby (200m): Yes'.format(item['Camera_Id'], item[color_prop0])
                    else:
                        item["tooltip"] = 'Camera {} <br/>Average speed along all lanes: {:.2f} <br/>Jam: No <br/>Incident nearby (200m): No'.format(item['Camera_Id'], item[color_prop0])

        else:
           return default_map


    geojson0 = dlx.dicts_to_geojson(dicts0, lon="Longitude", lat="Latitude")
    geobuf0 = dlx.geojson_to_geobuf(geojson0)
    vmax0 = df[color_prop0].max()
    colorbar0 = dl.Colorbar(colorscale=colorscale0, width=20, height=150, min=0, max=vmax0, unit='density per lane', opacity=0.9)
    geojson0 = dl.GeoJSON(data=geobuf0, id="geojson", format="geobuf",
                    zoomToBounds=True,  # when true, zooms to bounds when data changes
                    options=dict(pointToLayer=point_to_layer),  # how to draw points
                    superClusterOptions=dict(radius=50),   # adjust cluster size
                    hideout=dict(colorProp=color_prop0, circleOptions=dict(fillOpacity=0.7, stroke=False, radius=7),
                              min=0, max=vmax0, colorscale=colorscale0))
    fullmap = dl.Map([dl.TileLayer(url='https://maps-{s}.onemap.sg/v3/Grey/{z}/{x}/{y}.png', maxZoom=13, minZoom=12,
                             attribution='<img src="https://www.onemap.gov.sg/docs/maps/images/oneMap64-01.png" style="height:20px;width:20px;"/> OneMap | Map data &copy; contributors, <a href="http://SLA.gov.sg">Singapore Land Authority</a>'),
    geojson0, colorbar0], center=[1.3521, 103.8198],
                          style={'width': '90%', 'height': '80vh', 'margin': "auto", "display": "block", "position": "relative"},)


    return fullmap



if __name__ == '__main__':
    app.run_server(debug=True)


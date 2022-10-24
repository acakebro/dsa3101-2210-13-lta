'''
 # @ Create Time: 2022-10-08 23:39:32.168931
'''
import sys
import pathlib

sys.path.insert(1, "../../backend/Model/")

from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from datetime import datetime, date
import dash_leaflet as dl
import plotly.graph_objects as go
import dash_leaflet as dl
import os

traffic_incidents = pd.read_csv("traffic_incidents.csv")
traffic_speedbands = pd.read_csv("traffic_speedbands.csv")
traffic_images = pd.read_csv("traffic_images.csv")
#train_data = pd.read_csv("train_data.csv")

#cameras = [dict(title = str(traffic_images['CameraID'][0]),
#                position = [traffic_images['Latitude'][0],traffic_images['Longitude'][0]])]

cameras = [dict(center = [traffic_images['Latitude'][i],traffic_images['Longitude'][i]],
                children = [dl.Tooltip("Camera ID: " + str(traffic_images['CameraID'][i])), dl.Popup('Circle marker, 20px')],
               ) for i in range(len(traffic_images))]

folder = "assets/"

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

def create_Img(link_list):
    # Add a component that will render an image
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


'''
d_table_in = dash_table.DataTable(
            data=traffic_incidents.to_dict('records'),
            columns = [{"name": i, "id": i} for i in traffic_incidents.columns[:len(traffic_incidents.columns)-1]],
            cell_selectable=False,
            sort_action='native',
            filter_action='native',
            page_action = 'native',
            page_current = 0,
            page_size = 10
            )

d_table_sp = dash_table.DataTable(
            data=traffic_speedbands.to_dict('records'),
            columns = [{"name": i, "id": i} for i in traffic_speedbands.columns],
            cell_selectable=False,
            sort_action='native',
            filter_action='native',
            page_action = 'native',
            page_current = 0,
            page_size = 10
            )

d_table_im = dash_table.DataTable(
            data=traffic_images.to_dict('records'),
            columns = [{"name": i, "id": i} for i in traffic_images.columns],
            cell_selectable=False,
            sort_action='native',
            filter_action='native',
            page_action = 'native',
            page_current = 0,
            page_size = 10
            )
'''
layout = html.Div(children=[
    html.H1(children='Title', style = {'text-align':'center'}),
    html.Br(),

    # map
    html.Div(children = [
        dl.Map(children = [dl.TileLayer()] + [dl.CircleMarker(**i) for i in cameras],
               style={'width': '100%', 'height': '500px'},
              center=[1.3521, 103.8198],
              zoom = 11)
                  ]),
    html.Br(),

    # filter box
    html.Div(children = [
    html.H2("Select Region: ", style = {'margin':'5px'}),
    dcc.Dropdown(id = "region_dd",
                 options = [
            {'label':'North', 'value':'North'},
            {'label':'East', 'value':'East'},
            {'label':'West', 'value':'West'},
            {'label':'Central', 'value':'Central'},
            {'label':'North-East', 'value':'North-East'}],
                 style = {'display': 'inline-block', 'width':'200px', 'height': '30px',
                          'margin': '10px auto'}),
    html.Br(),
    html.H2("Select Direction: ", style = {'margin':'5px'}),
    dcc.Dropdown(id = "exp_dd",
                 options = [
            {'label': 'All' + " (" + str(len(os.listdir(folder))) + ")", 'value': 'All'},
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
                 style = {'display': 'inline-block', 'width':'200px', 'height': '30px',
                          'margin': '10px auto'})
    ], style = {'border': '1px solid black', 'width': '20%'}
             ),



    # time
    html.Div(
        html.H3("Time: " + datetime.now().strftime("%d/%m/%Y  %I:%M %p"),
                style = {'text-align': 'right',
                         'margin': '10px'})),

    # images
        html.Div(id = "img_out", style = {'text-align':'center', 'font-size':18})

    

    ],
                      style = {'background-color': 'rgb(237,250,252)'}
                      )
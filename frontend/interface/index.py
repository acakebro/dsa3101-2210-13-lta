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

from api_calls import ApiCall
api_obj = ApiCall("../interface")
api_obj.download_images()
api_obj.download_incidents()

import pg1,pg2,pg3
import callbacks
from maindash import app
import requests
camid = ['1001', '1002', '1003', '1004', '1005', '1006', '1501', '1502', '1503',
         '1504', '1505', '1701', '1702', '1703', '1704', '1705', '1706', '1707',
         '1709', '1711', '2701', '2702', '2703', '2704', '2705', '2706', '2707',
         '2708', '3702', '3704', '3705', '3793', '3795', '3796', '3797', '3798',
         '4701', '4702', '4703', '4704', '4705', '4706', '4707', '4708', '4709',
         '4710', '4712', '4713', '4714', '4716', '4798', '4799', '5794', '5795',
         '5797', '5798', '5799', '6701', '6703', '6704', '6705', '6706', '6708',
         '6710', '6711', '6712', '6713', '6714', '6715', '6716', '7791', '7793',
         '7794', '7795', '7796', '7797', '7798', '8701', '8702', '8704', '8706',
         '9701', '9702', '9703', '9704', '9705', '9706']

#api_obj = ApiCall("../app")
for i in camid:
    requests.get('http://127.0.0.1:5000/stats?live_image='+ i)


chroma = "https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"  # js lib used for colors

point_to_layer = assign("""function(feature, latlng, context){
    const {min, max, colorscale, circleOptions, colorProp} = context.props.hideout;
    const csc = chroma.scale(colorscale).domain([min, max]);  // chroma lib to construct colorscale
    circleOptions.fillColor = csc(feature.properties[colorProp]);  // set color based on color prop.
    return L.circleMarker(latlng, circleOptions);  // sender a simple circle marker.
    }""")

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



default_map = dl.Map([dl.TileLayer(url='https://maps-{s}.onemap.sg/v3/Grey/{z}/{x}/{y}.png', maxZoom=13, minZoom=12,

                             attribution='< img src="https://www.onemap.gov.sg/docs/maps/images/oneMap64-01.png" style="height:20px;width:20px;"/> OneMap | Map data &copy; contributors, <a href=" ">Singapore Land Authority</a >'),
    ], center=[1.3521, 103.8198],
                          style={'width': '90%', 'height': '80vh', 'margin': "auto", "display": "block", "position": "relative"},)


nav = Navbar()

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav, 
    html.Div(id='page-content', children=[]), 
])



if __name__ == '__main__':
    #app.run_server(host='0.0.0.0',debug=True, port=8050)
    app.run_server(debug=True, port = 8051)
    


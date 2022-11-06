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


#api_obj = ApiCall("../app")


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
    


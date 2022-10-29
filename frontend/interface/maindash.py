
import pandas as pd
from flask import Flask, jsonify, request, send_file
from datetime import datetime, date,timedelta
from api_calls import ApiCall
import requests
import dash
import dash_bootstrap_components as dbc


chroma = "https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"  # js lib used for colors
server = Flask(__name__)

app = dash.Dash(__name__, server=server,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                external_scripts = [chroma],
                meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                suppress_callback_exceptions=True)




from flask import Flask, jsonify, request, send_file
import pandas as pd
import glob

app = Flask(__name__)


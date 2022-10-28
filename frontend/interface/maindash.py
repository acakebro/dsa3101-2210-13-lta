
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



@app.server.route("/")
def run_main():
    main = Main()
    while True:
        api_obj = ApiCall("../interface")
        api_obj.download_images()
        startTime = datetime.datetime.now()
        print(f'{startTime}: Updating traffic stats...')
        main.update_stats()
        print(
            f'Stats updated. Time taken: {datetime.datetime.now() - startTime} minutes')
        print('Resting for 15 minutes...')
        time_wait = 15
        time.sleep(time_wait * 60)


# to be updated when finalised


@app.server.route("/stats", methods=["GET"])
def get_stats():
    camera_id = request.args.get('camera_id')
    df = pd.read_csv('traffic_stats.csv')
    match_df = df.loc[df['Camera_Id'] == int(camera_id)]
    result_df = match_df[['Density', 'Average_Speed', 'Incident']]
    return jsonify(result_df.to_dict(orient="records"))

# for past data
# to update to GET if filtering is required


@app.server.route("/archive")
def return_past_data():
    df = pd.read_csv('traffic_stats.csv')
    result_df = df[['Date', 'Time', 'Density', 'Average_Speed']]
    return jsonify(result_df.to_dict(orient="index"))

# for prediction based on user input


@app.server.route("/prediction", methods=["GET"])
def make_prediction():
    time = request.args.get('time')
    date = request.args.get('date')
    camera_id = int(request.args.get('camera_id'))
    road = request.args.get('road')
    model = pickle.load(open("model.pkl", "rb"))
    result = model.predict(camera_id, road, date, time)
    if result == 0:
        return jsonify({'prediction': 'No Jam'})
    elif result == 1:
        return jsonify({'prediction': 'Jam'})
    


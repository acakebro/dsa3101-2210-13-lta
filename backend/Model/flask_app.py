from flask import Flask, jsonify, request, send_file
import pandas as pd
from glob import glob
from main import Main
from RandomForest import RandomForestModel
import time
import datetime
import pickle

app = Flask(__name__)


@app.route("/live_image", methods=["GET"])
def return_live_image():
    camera_id = request.args.get('camera_id')
    for img_path in glob('./assets/*.jpg'):
        img_id = int(img_path.split("/")[-1].split("_")[0])
        if int(camera_id) == img_id:
            return send_file(img_path)

# to be updated when finalised

# for map stats (min, max, avg density + avg traffic speed)
@app.route("/stats", methods=["GET"])
def get_stats():
    selection = request.args.get('selection')
    df = pd.read_csv('traffic_stats.csv')
    if selection == 'max_traffic_density':
        result_df = df.sort_values('Density', ascending=False).drop_duplicates(subset='Camera_Id').sort_index()
        result_df = result_df[['Camera_Id', 'Direction', 'Latitude', 'Longitude', 'Jam', 'Density', 'Time']]
        return jsonify(result_df.to_dict(orient="records"))
    elif selection == 'min_traffic_density':
        result_df = df.sort_values('Density', ascending=True).drop_duplicates(subset='Camera_Id').sort_index()
        result_df = result_df[['Camera_Id', 'Direction', 'Latitude', 'Longitude', 'Jam', 'Density', 'Time']]
        return jsonify(result_df.to_dict(orient="records"))
    elif selection == 'average_traffic_density':
        result_df = df.groupby(['Camera_Id'])['Density'].mean().reset_index()
        result_df = result_df[['Camera_Id', 'Latitude', 'Longitude', 'Density', 'Time']]
        return jsonify(result_df.to_dict(orient="records"))
    elif selection == 'average_traffic_speed':
        result_df = df.groupby(['Camera_Id'])['Average_Speed'].mean().reset_index()
        result_df = result_df[['Camera_Id', 'Latitude', 'Longitude', 'Average_Speed', 'Time']]
        return jsonify(result_df.to_dict(orient="records"))

# for past data
@app.route("/archive")
def return_past_data():
    df = pd.read_csv('traffic_stats.csv')
    result_df = df[['Date', 'Time', 'Density', 'Average_Speed']]
    return jsonify(result_df.to_dict(orient="index"))

# for prediction based on user input


@app.route("/prediction", methods=["GET"])
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


@app.route("/")
def run_main():
    main = Main()
    while True:
        startTime = datetime.datetime.now()
        print(f'{startTime}: Updating traffic stats...')
        main.update_stats()
        print(
            f'Stats updated. Time taken: {datetime.datetime.now() - startTime} minutes')
        print('Resting for 30 minutes...')
        time_wait = 30
        time.sleep(time_wait * 60)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9001, debug=True)

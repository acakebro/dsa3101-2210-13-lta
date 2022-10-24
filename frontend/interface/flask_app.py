from flask import Flask, jsonify, request, send_file
import pandas as pd
import glob
from RandomForest import RandomForestModel

app = Flask(__name__)

@app.route("/live_image", methods=["GET"])
def return_live_image():
    camera_id = request.args.get('camera_id')
    for img_path in glob('./assets/*.jpg'):
        img_id = int(img_path.split("/")[-1].split("_")[0])
        if camera_id == img_id:
            return send_file(img_path)

# to be updated when finalised
@app.route("/stats", methods=["GET"])
def get_stats():
    camera_id = request.args.get('camera_id')
    df = pd.read_csv('archive.csv')
    match_df = df.loc[df['camera_id'] == camera_id]
    result_df = match_df[['Density', 'Average_Speed', 'Incident']]
    return jsonify(result_df.to_dict(orient="records"))

# for past data
# to update to GET if filtering is required
@app.route("/archive", methods=["GET"])
def return_past_data():
    camera_id = request.args.get('camera_id')
    df = pd.read_csv('archive.csv')
    match_df = df.loc[df['camera_id'] == camera_id]
    result_df = df[['Date', 'Time', 'Density', 'Average_Speed','Direction','Jam']]
    return jsonify(result_df.to_dict(orient="index"))

# for prediction based on user input
@app.route("/prediction", methods=["GET"])
def make_prediction():
    time = request.args.get('time')
    date = request.args.get('date')
    camera_id = request.args.get('camera_id')
    road = request.args.get('road')
    model = RandomForestModel('./training_data.csv', './camera_id_lat_long.csv')
    result = model.predict(camera_id, road, date, time)
    if result == 0:
        return jsonify({'prediction': 'No Jam'})
    elif result == 1:
        return jsonify({'prediction': 'Jam'})

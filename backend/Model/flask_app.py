from flask import Flask, jsonify, request, send_file
import pandas as pd
import glob

app = Flask(__name__)

@app.route("/live_image", methods=["GET"])
def return_live_image():
    camera_id = request.args.get('camera_id')
    for img_path in glob('./assets/*.jpg'):
        img_id = int(img_path.split("/")[-1].split("_")[0])
        if camera_id == img_id:
            return send_file(img_path)

@app.route("/stats", methods=["GET"])
def get_stats():
    camera_id = request.args.get('camera_id')
    df = pd.read_csv('test.csv')
    match_df = df.loc[df['camera_id'] == camera_id]
    result_df = match_df[['traffic_density', 'average_speed', 'traffic_incident']]
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/archive")
def return_past_data():
    df = pd.read_csv('archive.csv')
    result_df = df[['traffic_density', 'average_speed']]
    return jsonify(result_df.to_dict(orient="index"))
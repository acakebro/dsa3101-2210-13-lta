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


@app.route("/stats", methods=["GET"])
def get_stats():
    camera_id = request.args.get('camera_id')
    df = pd.read_csv('traffic_stats.csv')
    match_df = df.loc[df['Camera_Id'] == int(camera_id)]
    result_df = match_df[['Density', 'Average_Speed','Direction','Jam','Date','Time']]
    return jsonify(result_df.to_dict(orient="records"))

# for past data
# to update to GET if filtering is required


@app.route("/archive")
def return_past_data():
    df = pd.read_csv('traffic_stats.csv')
    result_df = df[['Camera_Id','Density', 'Average_Speed','Direction','Jam','Date','Time']]
    return jsonify(result_df.to_dict(orient="records"))

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
        print('Resting for 15 minutes...')
        time_wait = 15
        time.sleep(time_wait * 60)

@app.route("/incidents")
def get_incidents():
    uri = "http://datamall2.mytransport.sg"  # resource URL
    path = "/ltaodataservice/TrafficIncidents"
    headers = {
            "AccountKey": "AO4qMbK3S7CWKSlplQZqlA==",
            "accept": "application/json",
    }
    target = urlparse(uri + path)
    method = "GET"
    body = ""
    h = http.Http()
    response, content = h.request(target.geturl(), method, body, headers)
    jsonObj = json.loads(content)
    data = jsonObj["value"]
    return data

        
        
        
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

# encompass vehicle_count and caleb's random forest
from turtle import update
from api_calls import ApiCall
from vehicle_count import VehicleCount
import pandas as pd
import os
import time
import pickle


def update_stats():
    # needs to be full directory
    dir = '/Users/chuamingfeng/Desktop/NUS/Y3/S1/DSA3101/Project/training/api/2'
    api_call = ApiCall(dir)
    # downloads into api_data folder in your specified dir
    api_call.download_images()
    api_call.download_speedband()
    api_call.download_incidents()
    speedband_dir = dir + '/api_data/speedbands.csv'

    # can add a function to take nput from front end (must be most recent image to correspond with the newest speedband)
    images_dir = dir + '/api_data/*.jpg'
    incidents_dir = dir + '/api_data/incidents.csv'
    roi_df = 'ROI/Image_ROI.csv'  # Replace with final directory containing ROI file
    # Replace with final directory containing camera lat long file
    lat_long = 'camera_id_lat_long.csv'

    # change back to directory containing dnn weights
    os.chdir('/Users/chuamingfeng/Desktop/NUS/Y3/S1/DSA3101/Project')
    rf_model = pickle.load(open('model.pkl', 'rb'))
    vc = VehicleCount(images_dir, roi_df, lat_long,
                      speedband_dir, incidents_dir)
    traffic_stats = vc.predict_vehicle_count()
    for col in traffic_stats.dtypes[traffic_stats.dtypes == "object"].index:
        for_dummy = traffic_stats.pop(col)
        traffic_stats = pd.concat(
            [traffic_stats, pd.get_dummies(for_dummy, prefix=col)], axis=1)
    traffic_stats.to_csv('training_data/traffic_stats.csv',
                         mode='a', header=False, index=False)
    # removes response variables
    traffic_stats.pop("Jam")
    rf_model.predict(traffic_stats)
    test_pred = rf_model.predict(traffic_stats)
    traffic_stats["Jam"] = test_pred
    traffic_stats.to_csv('training_data/traffic_stats.csv',
                         mode='a', header=True, index=False)


update_stats()

"""
while True:
    update_stats()
    time_wait = 30
    time.sleep(time_wait * 60)
"""

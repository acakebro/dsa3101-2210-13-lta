# encompass vehicle_count and caleb's random forest
from api_calls import ApiCall
from vehicle_count import VehicleCount
import pandas as pd
import os

# needs to be full directory
dir = '/Users/chuamingfeng/Desktop/NUS/Y3/S1/DSA3101/Project/training/api/2'
api_call = ApiCall(dir)
# downloads into api_data folder in your specified dir
api_call.download_images()
api_call.download_speedband()
speedband_dir = dir + '/api_data/speedbands.csv'

# can add a function to take nput from front end (must be most recent image to correspond with the newest speedband)
images_dir = dir + '/api_data/*.jpg'
roi_df = 'ROI/Image_ROI.csv'  # Replace with final directory containing ROI file
# Replace with final directory containing camera lat long file
lat_long = 'camera_id_lat_long.csv'

# change back to directory containing dnn weights
os.chdir('/Users/chuamingfeng/Desktop/NUS/Y3/S1/DSA3101/Project')
vc = VehicleCount(images_dir, roi_df, lat_long, speedband_dir)
traffic_stats = vc.predict_vehicle_count()
print(traffic_stats)

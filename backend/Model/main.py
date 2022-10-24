# encompass vehicle_count and caleb's random forest
from turtle import update
from api_calls import ApiCall
from vehicle_count import VehicleCount
import os
import time
from datetime import datetime


class Main:
    def __init__(self):
        self.count = 1

    def update_stats(self):
        # needs to be full directory
        dir = '/Users/chuamingfeng/Desktop/NUS/Y3/S1/DSA3101/Project/training/api/test'
        api_call = ApiCall(dir)
        # downloads into api_data folder in your specified dir
        api_call.download_images()
        api_call.download_speedband()
        api_call.download_incidents()

        speedband_dir = dir + '/assets/speedbands.csv'
        speedband_cam_mapping_dir = 'closest_speedbands.csv'
        images_dir = dir + '/assets/*.jpg'
        incidents_dir = dir + '/assets/incidents.csv'
        roi_df = 'ROI/Image_ROI.csv'  # Replace with final directory containing ROI file
        # Replace with final directory containing camera lat long file
        lat_long = 'camera_id_lat_long.csv'

        # change back to directory containing dnn weights
        os.chdir('/Users/chuamingfeng/Desktop/NUS/Y3/S1/DSA3101/Project')
        vc = VehicleCount(images_dir, roi_df, lat_long,
                          speedband_dir, speedband_cam_mapping_dir, incidents_dir)
        traffic_stats = vc.predict_vehicle_count()
        if self.count == 1:
            traffic_stats.to_csv('training_data/traffic_stats.csv', mode='w+',
                                 header=True, index=False)
        else:
            traffic_stats.to_csv('training_data/traffic_stats.csv',
                                 mode='a', header=False, index=False)
        self.count += 1


main = Main()

while True:
    startTime = datetime.now()
    print(f"{startTime}: Updating traffic stats...")
    main.update_stats()
    print(f"Stats updated. Time taken: {datetime.now() - startTime} minutes")
    print("Resting for 5 minutes...")
    time_wait = 5
    time.sleep(time_wait * 60)

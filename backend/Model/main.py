from api_calls import ApiCall
from vehicle_count import VehicleCount
import os


class Main:
    def update_stats(self):
        # needs to be full directory
        dir = '/app'
        api_call = ApiCall(dir)
        # downloads into api_data folder in your specified dir
        api_call.download_images()
        api_call.download_speedband()
        api_call.download_incidents()

        speedband_dir = dir + '/assets/speedbands.csv'
        speedband_cam_mapping_dir = 'closest_speedbands.csv'
        images_dir = dir + '/assets/*.jpg'
        incidents_dir = dir + '/assets/incidents.csv'
        roi_df = dir + '/Image_ROI.csv'  # Replace with final directory containing ROI file
        # Replace with final directory containing camera lat long file
        lat_long = dir + '/camera_id_lat_long.csv'

        # change back to directory containing dnn weights
        os.chdir('/app')
        vc = VehicleCount(images_dir, roi_df, lat_long,
                          speedband_dir, speedband_cam_mapping_dir, incidents_dir)
        traffic_stats = vc.predict_vehicle_count()
        with open('traffic_stats.csv', 'a') as f:
            traffic_stats.to_csv(f, mode='a', index=False,
                                 header=f.tell() == 0)

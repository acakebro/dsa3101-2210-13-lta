import cv2
from glob import glob
from vehicle_detector import VehicleDetector
import pandas as pd
import ast
import numpy as np
from math import radians, cos, sin, asin, sqrt
import datetime


class VehicleCount:
    def __init__(self, images, image_roi_df, cam_lat_long, speedband_lat_long_df, speedband_cam_mapping, incidents_df):
        self.vehicle_detector = VehicleDetector()
        self.images = glob(images)
        self.image_roi_df = pd.read_csv(image_roi_df)
        self.cam_lat_long = pd.read_csv(cam_lat_long)
        self.speedband_lat_long_df = pd.read_csv(
            speedband_lat_long_df)
        self.speedband_cam_mapping = pd.read_csv(speedband_cam_mapping)
        self.incidents_df = pd.read_csv(incidents_df)
        self.incidents_df.rename(
            columns={'Latitude': 'AvgLat', 'Longitude': 'AvgLon'}, inplace=True)
        self.incidents_lat_long = self.incidents_df.iloc[:, 1:3].to_dict(
            "records")

    def __roi(self, img, coords):
        x = int(img.shape[1])
        y = int(img.shape[0])
        if len(coords) < 4:
            print("minimum 4 coordinates required")
            return
        shape = np.array(coords)  # Shape of roi
        mask = np.zeros_like(img)  # np array with zeros (of image dimension)

        # Creates a polygon with the mask colour (blue), areas not in roi would be black (pixel is 0)
        cv2.fillPoly(mask, pts=np.int32([shape]), color=(255, 255, 255))

        # Select areas where mask pixels are not zero
        masked_image = cv2.bitwise_and(img, mask)
        return masked_image

    # Distance between 2 geographical locations
    def __distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance in meters between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        # Radius of earth in meters.
        r = 6.371e6
        return c * r

    # Finds index of speedband df where the corresponding Lat long is closest to given camera coordinates
    def __closest(self, data, cam_coords):
        lat_long = min(
            data,
            key=lambda p: self.__distance(
                cam_coords["Latitude"],
                cam_coords["Longitude"],
                p["AvgLat"],
                p["AvgLon"],
            )
        )
        index = data.index(lat_long)
        distance = self.__distance(
            cam_coords["Latitude"],
            cam_coords["Longitude"],
            lat_long["AvgLat"],
            lat_long["AvgLon"],
        )
        return [index, lat_long, distance]

    def __time_in_range(self, start, end, x):
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end

    def __is_weekday(self, image_datetime):
        day = image_datetime.weekday()
        if day < 5:  # Monday(0) to Friday(4)
            return 1
        return 0

    def __is_peak(self, image_datetime):
        peak_hours = [
            {"Start": datetime.time(8, 0, 0), "End": datetime.time(10, 0, 0)},
            {"Start": datetime.time(18, 0, 0),
             "End": datetime.time(20, 30, 0)},
        ]
        is_peak_bool = False
        for peak_hour in peak_hours:
            if is_peak_bool:
                break
            start, end = peak_hour.get("Start"), peak_hour.get("End")
            is_peak_bool = self.__time_in_range(
                start, end, image_datetime.time())
        if is_peak_bool:
            return 1
        return 0

    def predict_vehicle_count(self):
        result_list = []
        for img_path in self.images:
            camera_id = int(img_path.split("/")[-1].split("_")[0])
            timestamp = img_path.split("/")[-1].split("_")[2]
            image_datetime = datetime.datetime.strptime(
                timestamp, "%Y%m%d%H%M%S")
            is_peak = self.__is_peak(image_datetime)
            is_weekday = self.__is_weekday(image_datetime)
            rois = self.image_roi_df[self.image_roi_df.Camera_Id == camera_id]
            # Coordinates of cam {Latitude: ..., Longitude: ...}
            cam_coords = (
                self.cam_lat_long[self.cam_lat_long.CameraID == camera_id]
                .iloc[:, -2:]
                .to_dict("records")[0]
            )
            # Index to retrieve the average speed from speedband df
            speedband_link_id = self.speedband_cam_mapping[
                self.speedband_cam_mapping.CameraID == camera_id].iloc[0, -1]
            avg_speed = self.speedband_lat_long_df[self.speedband_lat_long_df.LinkID ==
                                                   speedband_link_id].iloc[0, 7]
            closest_incident = self.__closest(
                self.incidents_lat_long, cam_coords)
            incident_distance = closest_incident[2]
            incident = 0
            if incident_distance <= 200:
                incident = 1
            img = cv2.imread(img_path)
            for i in range(len(rois)):
                roi_coords = ast.literal_eval(rois.iloc[i, 1])
                direction = rois.iloc[i, 2]
                roi_img = self.__roi(img, roi_coords)
                vehicle_boxes = self.vehicle_detector.detect_vehicles(roi_img)
                vehicle_count = len(vehicle_boxes)
                density = vehicle_count / (0.100 * 3)
                # Approximate length of road to be 100m with an average of 3 lanes
                jam = 0
                if avg_speed <= 30 or density >= 0.07:
                    jam = 1
                result_list.append(
                    [
                        camera_id,
                        direction,
                        vehicle_count,
                        density,
                        avg_speed,
                        image_datetime.date(),
                        image_datetime.time(),
                        cam_coords.get("Latitude"),
                        cam_coords.get("Longitude"),
                        is_weekday,
                        is_peak,
                        incident,
                        incident_distance,
                        jam
                    ]
                )
        result_df = pd.DataFrame(
            result_list,
            columns=[
                "Camera_Id",
                "Direction",
                "Vehicle_Count",
                "Density",
                "Average_Speed",
                "Date",
                "Time",
                "Latitude",
                "Longitude",
                "Is_Weekday",
                "Is_Peak",
                "Incident",
                "Closest_Incident_Distance",
                "Jam"
            ],
        )
        return result_df

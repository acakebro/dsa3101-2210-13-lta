import cv2
from glob import glob
from vehicle_detector import VehicleDetector
import pandas as pd
import ast
import numpy as np
from math import radians, cos, sin, asin, sqrt
import datetime


class VehicleCount:
    def __init__(self, images, image_roi_df, cam_lat_long, speedband_lat_long_df, incidents_df):
        self.vehicle_detector = VehicleDetector()
        self.images = glob(images)  # to input through main
        self.image_roi_df = pd.read_csv(image_roi_df)  # to input through main
        self.cam_lat_long = pd.read_csv(cam_lat_long)  # to input through main
        self.speedband_lat_long_df = pd.read_csv(
            speedband_lat_long_df)  # to input through main
        self.speedband_lat_long = self.speedband_lat_long_df.iloc[:, -2:].to_dict(
            "records")
        self.incidents_df = pd.read_csv(incidents_df)
        self.incidents_df.rename(
            columns={'Latitude': 'AvgLat', 'Longitude': 'AvgLon'}, inplace=True)
        self.incidents_lat_long = self.incidents_df.iloc[:, 1:3].to_dict(
            "records")

    def __display_image(self, img_name, img):
        cv2.namedWindow(img_name, cv2.WINDOW_NORMAL)  # Fit image to window
        cv2.imshow(img_name, img)
        cv2.waitKey()
        cv2.destroyAllWindows()

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
        Calculate the great circle distance in kilometers between two points 
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

    def __is_peak(self, is_peak_boolean):
        if is_peak_boolean:
            return 1
        return 0

    def display(self):
        for img_path in self.images:
            camera_id = int(img_path.split("/")[-1].split("_")[0])
            rois = self.image_roi_df[self.image_roi_df.Camera_Id == camera_id]
            img = cv2.imread(img_path)
            for i in range(len(rois)):
                roi_coords = ast.literal_eval(rois.iloc[i, 1])
                roi_img = self.__roi(img, roi_coords)
                vehicle_boxes = self.vehicle_detector.detect_vehicles(roi_img)
                vehicle_count = len(vehicle_boxes)
                # width then height
                for box in vehicle_boxes:
                    x, y, w, h = box
                    cv2.rectangle(roi_img, (x, y),
                                  (x + w, y + h), (25, 0, 180), 3)
                    cv2.putText(
                        roi_img,
                        "Count:" + str(vehicle_count),
                        (1600, 1000),
                        2,
                        2,
                        (0, 102, 240),
                        4,
                    )
                cv2.imshow("LTA", roi_img)
                # keep image on hold
                cv2.waitKey(1)

    def predict_vehicle_count(self):
        result_list = []
        peak_hours = [
            {"Start": datetime.time(8, 0, 0), "End": datetime.time(10, 0, 0)},
            {"Start": datetime.time(18, 0, 0),
             "End": datetime.time(20, 30, 0)},
        ]
        for img_path in self.images:
            is_peak_bool = False
            camera_id = int(img_path.split("/")[-1].split("_")[0])
            timestamp = img_path.split("/")[-1].split("_")[2]
            image_datetime = datetime.datetime.strptime(
                timestamp, "%Y%m%d%H%M%S")
            for peak_hour in peak_hours:
                if is_peak_bool:
                    break
                start, end = peak_hour.get("Start"), peak_hour.get("End")
                is_peak_bool = self.__time_in_range(
                    start, end, image_datetime.time())
            is_peak = self.__is_peak(is_peak_bool)
            is_weekday = self.__is_weekday(image_datetime)
            rois = self.image_roi_df[self.image_roi_df.Camera_Id == camera_id]
            # Coordinates of cam {Latitude: ..., Longitude: ...}
            cam_coords = (
                self.cam_lat_long[self.cam_lat_long.CameraID == camera_id]
                .iloc[:, -2:]
                .to_dict("records")[0]
            )
            # Index to retrieve the average speed from speedband df
            closest_speedband_index = self.__closest(
                self.speedband_lat_long, cam_coords)[0]
            closest_incident = self.__closest(
                self.incidents_lat_long, cam_coords)
            incident_distance = closest_incident[2]
            incident_type = None
            if incident_distance > 100:
                closest_incident_index = closest_incident[0]
                incident_type = self.incidents_df.iloc[closest_incident_index, 0]
            avg_speed = self.speedband_lat_long_df.iloc[closest_speedband_index, 7]
            img = cv2.imread(img_path)
            for i in range(len(rois)):
                roi_coords = ast.literal_eval(rois.iloc[i, 1])
                direction = rois.iloc[i, 2]
                roi_img = self.__roi(img, roi_coords)
                vehicle_boxes = self.vehicle_detector.detect_vehicles(roi_img)
                vehicle_count = len(vehicle_boxes)
                Is_Jam = 0
                if vehicle_count > 0:
                    if avg_speed <= 35:
                        Is_Jam = 1
                # Approximate length of road to be 100m
                result_list.append(
                    [
                        camera_id,
                        direction,
                        vehicle_count,
                        vehicle_count / 100,
                        avg_speed,
                        image_datetime.date(),
                        image_datetime.time(),
                        cam_coords.get("Latitude"),
                        cam_coords.get("Longitude"),
                        is_weekday,
                        is_peak,
                        incident_type,
                        Is_Jam
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
                "Incident_Type",
                "Jam"
            ],
        )
        return result_df

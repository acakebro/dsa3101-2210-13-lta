import cv2
from glob import glob
from vehicle_detector import VehicleDetector
import pandas as pd
import ast
import numpy as np


class VehicleCount:

    def __init__(self, images, image_roi_df, lat_long):
        self.vehicle_detector = VehicleDetector()
        self.images = glob(images)
        self.image_roi_df = pd.read_csv(image_roi_df)
        self.lat_long = pd.read_csv(lat_long)

    def display_image(self, img_name, img):
        cv2.namedWindow(img_name, cv2.WINDOW_NORMAL)  # fit image to window
        cv2.imshow(img_name, img)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def roi(self, img, coords):
        x = int(img.shape[1])
        y = int(img.shape[0])
        if len(coords) < 4:
            print('minimum 4 coordinates required')
            return
        shape = np.array(coords)  # shape of roi
        mask = np.zeros_like(img)  # np array with zeros (of image dimension)

        # creates a polygon with the mask colour (blue), areas not in roi would be black (pixel is 0)
        cv2.fillPoly(mask, pts=np.int32([shape]), color=(255, 255, 255))

        # select ares where mask pixels are not zero
        masked_image = cv2.bitwise_and(img, mask)
        return masked_image

    def display(self):
        for img_path in self.images:
            camera_id = int(img_path.split('/')[-1].split('_')[0])
            rois = self.image_roi_df[self.image_roi_df.Camera_Id == camera_id]
            img = cv2.imread(img_path)
            for i in range(len(rois)):
                roi_coords = ast.literal_eval(rois.iloc[i, 1])
                roi_img = self.roi(img, roi_coords)
                vehicle_boxes = self.vehicle_detector.detect_vehicles(roi_img)
                vehicle_count = len(vehicle_boxes)
                # width then height
                for box in vehicle_boxes:
                    x, y, w, h = box
                    cv2.rectangle(roi_img, (x, y),
                                  (x + w, y + h), (25, 0, 180), 3)
                    cv2.putText(
                        roi_img, "Count:" + str(vehicle_count), (1600,
                                                                 1000), 2, 2, (0, 102, 240), 4
                    )
                cv2.imshow("LTA", roi_img)
                # keep image on hold
                cv2.waitKey(1)

    def predict_vehicle_count(self):
        result_list = []
        for img_path in self.images:
            camera_id = int(img_path.split('/')[-1].split('_')[0])
            timestamp = img_path.split('/')[-1].split('_')[2]
            rois = self.image_roi_df[self.image_roi_df.Camera_Id == camera_id]
            lat = self.lat_long[self.lat_long.CameraID ==
                                camera_id].iloc[0].Latitude
            long = self.lat_long[self.lat_long.CameraID ==
                                 camera_id].iloc[0].Longitude
            img = cv2.imread(img_path)
            for i in range(len(rois)):
                roi_coords = ast.literal_eval(rois.iloc[i, 1])
                direction = rois.iloc[i, 2]
                roi_img = self.roi(img, roi_coords)
                vehicle_boxes = self.vehicle_detector.detect_vehicles(roi_img)
                vehicle_count = len(vehicle_boxes)
                result_list.append(
                    [camera_id, direction, vehicle_count, vehicle_count/150, timestamp, lat, long])
        result_df = pd.DataFrame(result_list, columns=[
            'Camera_Id', 'Direction', 'Vehicle_Count', 'Density', 'Timestamp', 'Latitude', 'Longitude'])
        return result_df


### TESTS ###
images_dir = 'sharepoint/2022_01_05_22_00/1701_2153_20220105215500_fab0b3.jpg'
roi_df = 'ROI/Image_ROI.csv'
lat_long = 'camera_id_lat_long.csv'
vc = VehicleCount(images_dir, roi_df, lat_long)
print(vc.predict_vehicle_count())
#############

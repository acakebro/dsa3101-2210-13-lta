import cv2
import os
import glob  # allows us to load all the path of all the files in a folder
from vehicle_detector import VehicleDetector
import pandas as pd
import ast
import numpy as np


def display_image(img_name, img):
    cv2.namedWindow(img_name, cv2.WINDOW_NORMAL)  # fit image to window
    cv2.imshow(img_name, img)
    cv2.waitKey()
    cv2.destroyAllWindows()


def roi(img, coords):
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


print(os.getcwd())  # .../dsa3101-2210-13-lta

# Load Vehicle Detector
vd = VehicleDetector()  # instantiate the instance

# Load images from a folder
images_folder = glob.glob("sharepoint/2022_01_05_22_00/*.jpg")
print(images_folder)  # check for all the paths of the images

vehicles_folder_count = 0

# file containing all the roi boundary boxes and direction labels
image_roi_df = pd.read_csv('ROI/Image_ROI.csv')

# Lopp through all the images
for img_path in images_folder:
    camera_id = int(img_path.split('/')[-1].split('_')[0])
    rois = image_roi_df[image_roi_df.Camera_Id == camera_id]
    img = cv2.imread(img_path)
    for i in range(len(rois)):
        roi_coords = ast.literal_eval(rois.iloc[i, 1])
        direction = rois.iloc[i, 2]
        roi_img = roi(img, roi_coords)
        vehicle_boxes = vd.detect_vehicles(roi_img)
        print(vehicle_boxes)  # the coordinates of each car
        vehicle_count = len(vehicle_boxes)
        # width then height
        for box in vehicle_boxes:
            x, y, w, h = box
            cv2.rectangle(roi_img, (x, y), (x + w, y + h), (25, 0, 180), 3)

            cv2.putText(
                roi_img, "Count:" + str(vehicle_count), (1600,
                                                         1000), 2, 2, (0, 102, 240), 4
            )

        cv2.imshow("LTA", roi_img)
        # keep image on hold
        cv2.waitKey(1)

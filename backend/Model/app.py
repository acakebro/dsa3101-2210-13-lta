import cv2
import os
import glob  # allows us to load all the path of all the files in a folder
from vehicle_detector import VehicleDetector

print(os.getcwd())  # .../dsa3101-2210-13-lta

# Load Vehicle Detector
vd = VehicleDetector()  # instantiate the instance

# Load images from a folder
images_folder = glob.glob("images/*.jpg")
print(images_folder)  # check for all the paths of the images

vehicles_folder_count = 0

# Lopp through all the images
for img_path in images_folder:
    img = cv2.imread(img_path)
    vehicle_boxes = vd.detect_vehicles(img)
    print(vehicle_boxes)  # the coordinates of each car
    vehicle_count = len(vehicle_boxes)
    # width then height
    for box in vehicle_boxes:
        x, y, w, h = box
        cv2.rectangle(img, (x, y), (x + w, y + h), (25, 0, 180), 3)

        cv2.putText(
            img, "Count:" + str(vehicle_count), (1600, 1000), 2, 2, (0, 102, 240), 4
        )

    cv2.imshow("LTA", img)
    # keep image on hold
    cv2.waitKey(1)

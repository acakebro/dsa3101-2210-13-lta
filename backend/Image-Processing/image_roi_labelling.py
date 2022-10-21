import cv2
import numpy as np
from glob import glob
import pandas as pd


class ShapeCoords:
    def __init__(self, img):
        self.points = []
        self.img = img

    def click_event(self, event, x, y, flags, params):
        # checking for left mouse clicks, display in shell if found
        if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_RBUTTONDOWN:
            self.points.append((x, y))
            # print(x, ' ', y)
            # displaying the coordinates on the image window
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = '(' + str(x) + ', ' + str(y) + ')'
            display_img = self.img.copy()
            cv2.putText(display_img, text, (x, y), font, 0.8, (255, 0, 0), 2)
            cv2.imshow('image', display_img)


class ImageLabel:
    def __init__(self, label_file, images):
        self.img_paths = glob(images)
        self.result_list = []
        self.labels_dict = None
        self.__process_labels(label_file)

    def __process_labels(self, label_file):
        labels_df = pd.read_csv(label_file)
        labels_df.Labels = labels_df.Labels.apply(
            lambda x: list(map(lambda y: y.upper(), x.split(';'))))
        self.labels_dict = dict(zip(labels_df.Camera_Id, labels_df.Labels))

    def label(self):
        result_list = []
        for img_path in self.img_paths:
            camera_id = int(img_path.split(
                '/')[-1].split('.')[0].split('_')[0])
            labels = self.labels_dict.get(camera_id)
            img = cv2.imread(img_path)
            camera_location = []
            for label in labels:
                shape_coords = ShapeCoords(img)
                # fit image to window
                cv2.namedWindow('image', cv2.WINDOW_NORMAL)
                cv2.setMouseCallback('image', shape_coords.click_event)
                cv2.imshow('image', img)
                cv2.waitKey()
                cv2.destroyAllWindows()
                road_name = input('Enter the road direction: ').strip().upper()
                camera_location = [camera_id, shape_coords.points, road_name]
                result_list.append(camera_location)
        result_df = pd.DataFrame(result_list, columns=[
                                 'Camera_Id', 'ROI', 'Direction'])
        result_df.to_csv('Image_ROI5.csv', index=False)

### TESTS ###


label_file = 'label_filters.csv'
images = 'sharepoint/2022_01_05_22_00/Split/4/*'
ImageLabel = ImageLabel(label_file, images)
ImageLabel.label()

#############

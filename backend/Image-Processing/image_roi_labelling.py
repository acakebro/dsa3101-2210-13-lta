import cv2
import numpy as np

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


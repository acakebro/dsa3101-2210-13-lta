'''
code reference: 
https://docs.opencv.org/3.4/d3/dc1/tutorial_basic_linear_transform.html

colour brightness formula (checkpoint 2.2):
https://www.w3.org/TR/AERT/#color-contrast
'''

from PIL import Image, ImageStat
import cv2
import numpy as np
import math as Math

# measure brightness (ITU-R BT.601 standard) for jpeg image
def measure_img_brightness(img_path):
    img = Image.open(img_path)
    stat = ImageStat.Stat(img)
    r, g, b = stat.mean
    y = 0.299*r + 0.587*g + 0.116*b
    # print(y)
    # set threshold for images (user chosen)
    # min: 0 (black), max: 255 (white)
    threshold = 150
    # find a better way to get alpha & beta?
    alpha = round(threshold/y, 1) # controls brightness
    beta = round(threshold - alpha*y, 0) # controls contrast
    return [alpha, beta]

# resizing image is optional
# used to make sure can see old & new image side to side
def resize_image(img):
    width = int(img.shape[1])
    height = int(img.shape[0])
    if (width > 800 or height > 800):
        ratio = 800/width
        dim = (int(width*ratio), int(height*ratio))
        image_resize = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        # new_image_resize = new_img.resize(new_img, dim)
    else:
        image_resize = img
        # new_image_resize = new_img
    return image_resize

img_path = r"C:\Users\renac\Downloads\NUS\Y3S1\DSA3101\project\images\2022_01_05_21_10\1701_2103_20220105210501_22826b.jpg"
alpha, beta = measure_img_brightness(img_path)
image = cv2.imread(img_path)

if image is None:
    print('Could not open or find the image')
    exit(0)

img_resize = resize_image(image)
new_image = np.zeros(img_resize.shape, image.dtype)

# faster method with new_image(i,j) = alpha*image(i,j) + beta
new_image = cv2.convertScaleAbs(img_resize, alpha=alpha, beta=beta)

img_corrected = cv2.hconcat([img_resize, new_image])

# access pixels manually and convert
# for y in range(image.shape[0]):
#     for x in range(image.shape[1]):
#         for c in range(image.shape[2]):
#             new_image[y,x,c] = np.clip(alpha*image[y,x,c] + beta, 0, 255)

# uncomment to write image out
# cv2.imwrite("new_bright_img.jpg", new_image)
cv2.imshow('Original vs New', img_corrected)
cv2.waitKey()

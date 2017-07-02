import os
import cv2
import glob
import numpy as np
from matplotlib import pyplot as plt

loc = None
colors = [128, 128, 128]
def get_rgb(mouse_event, x_pos, y_pos, flags, param):
    global loc, colors
    if mouse_event == 1:
        loc = x_pos, y_pos
    if mouse_event == 4:
        print("[+]RGB values are", list(img[loc[1], loc[0], :]))
        colors = list(img[loc[1], loc[0], :])



cv2.namedWindow("Image", 1)
cv2.setMouseCallback("Image", get_rgb)
img = cv2.imread("chassis_1.jpg", 1)
while True:
    r, g, b = colors
    print(r, g, b)
    lower = np.array([r - 50, g - 50, b - 50], dtype="uint8")
    upper = np.array([r + 50, g + 50, b + 50], dtype="uint8")
    mask = cv2.inRange(img, lower, upper)
    roi = cv2.bitwise_and(img, img, mask=mask)
    cv2.imshow("Image", np.hstack([img, roi]))
    if cv2.waitKey() == 27:
        break
        # cv2.destroyAllWindows()
        # exit(0)
cv2.destroyAllWindows()
# list(image[50,50,:]) returns BGR values of the point


import os
import cv2
import glob
import numpy as np
from matplotlib import pyplot as plt
from bolt_detection import equalizeHistColor
from multiprocessing import Process


loc = None
colors = [128, 128, 128]
pal = False


def nil(n):
    pass


def get_rgb(mouse_event, x_pos, y_pos, flags, param):
    global loc, colors
    if mouse_event == 1:
        loc = x_pos, y_pos
    if mouse_event == 4:
        print("[+]RGB values are " + ' '.join(str(item) for item in list(img[loc[1], loc[0], :])[::-1])
              + " at " + str(x_pos) + " " + str(y_pos))
        colors = list(img[loc[1], loc[0], :])[::-1]  # BGR


# def correct():
def palette():
    background = np.zeros((320, 240, 3), np.uint8)
    cv2.namedWindow('Palette')
    cv2.createTrackbar('R', 'Palette', 0, 255, nil)
    cv2.createTrackbar('G', 'Palette', 0, 255, nil)
    cv2.createTrackbar('B', 'Palette', 0, 255, nil)
    global colors
    # cv2.createButton('ON/OFF', nil)
    while True:
        print("Running Palette Thread")
        cv2.imshow('Palette', background)
        if cv2.waitKey(1) == 113:
            break
        pr = cv2.getTrackbarPos('R', 'Palette')
        pg = cv2.getTrackbarPos('G', 'Palette')
        pb = cv2.getTrackbarPos('B', 'Palette')
        # cv2.circle(background, (160, 120), 50, (0, 0, 255), 1)
        cv2.circle(background, (120, 160), 50, (pb, pg, pr), -1)  # Filled
        # background[:] = [b, g, r]
        colors = pb, pg, pr


cv2.namedWindow("Image", 1)
cv2.setMouseCallback("Image", get_rgb)
img = cv2.imread("chassis_1.jpg", 1)
# img = equalizeHistColor(img)
while True:
    # print("Running Main Thread")
    r, g, b = colors
    # print(r, g, b)
    lower = np.array([b - 50, g - 50, r - 50], dtype="uint8")
    upper = np.array([b + 50, g + 50, r + 50], dtype="uint8")
    mask = cv2.inRange(img, lower, upper)
    roi = cv2.bitwise_and(img, img, mask=mask)
    cv2.imshow("Image", np.hstack([img, roi]))
    if cv2.waitKey(1) == 27:   # Redraw
        break
    if cv2.waitKey(1) == 112:
        if pal is False:
            pr1 = Process(target=palette)
            pr1.start()
            pr1.join()
            pal = True
        else:
            cv2.destroyWindow('Palette')
            pal = False
        # cv2.destroyAllWindows()
        # exit(0)
cv2.destroyAllWindows()

# 51 167 174 low bolt left
# list(image[50,50,:]) returns BGR values of the point
# a, b are the top - left coordinate of the rectangle and (c, d) be its width and height.OpenCV Contour Features
# To judge a point(x0, y0) is in the rectangle, just to check if a < x0 < a + c and b < y0 < b + d


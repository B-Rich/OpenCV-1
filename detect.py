import os
import cv2
import glob
import numpy as np
from matplotlib import pyplot as plt


image = cv2.imread('chassis_1.jpg', 0)
img = image.copy()
# image = cv2.cvtColor(image, 6)  # BGR to Gray
# image = cv2.Canny(image, 50, 200)
child_dir = next(os.walk('.'))[1]

# lower = np.array([0, 0, 0])
# upper = np.array([15, 15, 15])
# shapeMask = cv2.inRange(image, lower, upper)
# for folder in child_dir
folder = child_dir[2]
for file in glob.glob(os.path.join('.\\' + folder, '*.*')):
    extension = os.path.splitext(file)[1][1:]  # Check if files are actually an image file
    if extension == 'jpg' or extension == 'png' or extension == 'bmp':
        template = cv2.imread(file, 0)
        cv2.imshow("Template", template)
        # template = cv2.cvtColor(template, 6)  # BGR to Gray
        # template = cv2.Canny(template, 50, 200)
        (tp_h, tp_w) = template.shape[::-1]  # [:2]
        match = cv2.matchTemplate(image, template, 1)  # Normalized square difference
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
        # upper_left = min_loc
        lower_right = (min_loc[0] + tp_w, min_loc[1] + tp_h)
        cv2.rectangle(img, min_loc, lower_right, 255, 2)
        plt.subplot(121), plt.imshow(match, cmap='gray')
        plt.title('Match'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(img, cmap='gray')
        plt.title('Point'), plt.xticks([]), plt.yticks([])
        plt.show()


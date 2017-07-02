import cv2
import numpy as np

def nil(n):
    pass

background = np.zeros((320, 240, 3), np.uint8)
cv2.namedWindow('Palette')

cv2.createTrackbar('R', 'Palette', 0, 255, nil)
cv2.createTrackbar('G', 'Palette', 0, 255, nil)
cv2.createTrackbar('B', 'Palette', 0, 255, nil)
# cv2.createButton('ON/OFF', nil)
while True:
    cv2.imshow('Palette', background)
    if cv2.waitKey(1) == 27:
        break
    r = cv2.getTrackbarPos('R', 'Palette')
    g = cv2.getTrackbarPos('G', 'Palette')
    b = cv2.getTrackbarPos('B', 'Palette')
    # cv2.circle(background, (160, 120), 50, (0, 0, 255), 1)
    # cv2.setTrackbarPos('R', 'Palette', fun[0])
    # cv2.setTrackbarPos('G', 'Palette', fun[1])
    # cv2.setTrackbarPos('B', 'Palette', fun[2])
    background[:] = [b, g, r]
cv2.destroyAllWindows()


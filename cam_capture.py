import cv2
import sys
import time
import datetime
import os

def main(argv):
    cap = cv2.VideoCapture(0)
    test = cap.get(0)  # CV_CAP_PROP_POS_MSEC
    ratio = cap.get(2)  # CV_CAP_PROP_POS_AVI_RATIO
    width = cap.get(3)  # CV_CAP_PROP_FRAME_WIDTH
    height = cap.get(4)  # CV_CAP_PROP_FRAME_HEIGHT
    frame_rate = cap.get(5)  # CV_CAP_PROP_FPS
    brightness = cap.get(10)  # CV_CAP_PROP_BRIGHTNESS
    contrast = cap.get(11)  # CV_CAP_PROP_CONTRAST
    print("Test: ", test)
    print("Ratio: ", ratio)
    print("Frame Rate: ", frame_rate)
    print("Height: ", height)
    print("Width: ", width)
    print("Brightness: ", brightness)
    print("Contrast: ", contrast)
    directory = "captures"
    i = 0
    while True:
        ret, feed = cap.read()
        cv2.imshow("Camera Feed", feed)

        key = cv2.waitKey(10)
        if key == 27:
            break
        if key == 115:
            f = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H%M%S')
            if not os.path.exists(directory):
                os.makedirs(directory)
            retf = cv2.imwrite(directory + "\\" + f + ".jpg", feed, [1, 100])
            print("Captured: ", retf)
            i += 1

    cv2.destroyAllWindows()
    cv2.VideoCapture(0).release()

if __name__ == '__main__':
    main(sys.argv)

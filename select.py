import cv2
import sys
import time
import datetime
import os


s_start = None
s_region = (0, 0, 0, 0)
img = None


def select_region(mouse_event, x_pos, y_pos, flags, param):
    global s_start, s_region
    if mouse_event == 1:  # Left mouse button down, starting selection
        s_start = x_pos, y_pos
        s_region = 0, 0, 0, 0  # x1, y1, x2, y2
    elif mouse_event == 4:  # Left mouse button up, selection finished
        if s_region[2] > s_region[0] and s_region[3] > s_region[1]:
            selection = temp[s_region[1]:s_region[3], s_region[0]:s_region[2]]
            cv2.imshow("Selection", selection)
            sel_name = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H%M%S')
            if not os.path.exists(directory):
                os.makedirs(directory)
            cv2.imwrite(directory + "\\" + sel_name + ".jpg", selection, [1, 100])
            print("[+]Selection done!")
        s_start = None
    elif s_start:
        if flags & 1:  # Left button was actually presed
            x1 = min(s_start[0], x_pos)
            y1 = min(s_start[1], y_pos)
            x2 = max(s_start[0], x_pos)
            y2 = max(s_start[1], y_pos)
            s_region = x1, y1, x2, y2
            img = cv2.cvtColor(temp, 3)  # Greyscale to color, 8
            cv2.rectangle(img, (s_region[0], s_region[1]), (s_region[2], s_region[3]), (255, 0, 0), 1)
            cv2.imshow("Image", img)
        else:
            print("[+]Selection done!")
            s_start = None


if __name__ == '__main__':
    directory = "Optra"
    cv2.namedWindow("Image", 1)
    cv2.setMouseCallback("Image", select_region)
    img = cv2.imread("chassis_1.jpg", 1)
    temp = cv2.cvtColor(img, 0)  # Color to Greyscale, 6 ,3
    cv2.imshow("Image", img)
    if cv2.waitKey() == 27:
        cv2.destroyAllWindows()
        exit(0)


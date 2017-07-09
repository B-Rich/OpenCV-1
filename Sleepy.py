import cv2
import dlib
import time
import datetime
import numpy as np
import playsound as ps
from threading import Thread
from pygame import mixer as mx
from EyeSpy import EyeSpy as ispy
from multiprocessing import Process
from collections import OrderedDict
from scipy.spatial import distance as d


#Data stored will be used for slicing and thus inclusiveness and exclusiveness must be taken into account
fac_land = OrderedDict([("left_brow",(17, 22))  # 18 to 22
, ("right_brow",(22, 27))  # 23 to 27
, ("jaw",(0, 17))  # 1 to 17
, ("left_eye",(36, 42))  # 37 to 42
, ("right_eye",(42, 48))  # 43 to 48
, ("nose",(27, 36))  # 28 to 36
, ("mouth",(48, 68))])  # 49 to 68

awake = False
ticks = 0

# return (arg.left(), arg.top(), arg.right() - arg.left(), arg.bottom() - arg.top())

def npa(marks):
    points = np.zeros((68,2), dtype='int')
    for loc in range(0, 68):
        points[loc] = (marks.part(loc).x, marks.part(loc).y)
    return points

def alarm():
    # mx.init()
    # mx.music.load('D:/Users/Threadcount/Desktop/OpenCV Trials/Bot/C.mp3')
    # mx.music.play()
    # ps.playsound('./C.mp3', True)
    ps.playsound('D:/Users/Threadcount/Desktop/OpenCV Trials/Bot/C.mp3', True)

#The eye's condition using this dataset should be computed by finding the distance between
#points (37,40) (x), (38,42) and (39,41) (y)
#If the eyes are closed, the distance between the points that are parallel to the Y-axis should be so small approx. 0
#The X part should not change as an eye's width does not change

def open_ratio(i):
    X = d.euclidean(i[0], i[3])
    Y1 = d.euclidean(i[1], i[5])
    Y2 = d.euclidean(i[2], i[4])
    return (Y1 + Y2) / (2.0 * X)  # Change factor

def sleepy(ratio, img):
    global ticks, awake
    if ratio < 0.27:
        ticks += 1
        if ticks >= 40:
            if not awake:
                awake = True
                tr = Thread(target=alarm, args=())
                tr.daemon = True
                tr.start()
            cv2.putText(img, "[+]Sleepy head detected!", (20, 40), 6, 0.7, (0, 255, 255), 2)
    else:
        ticks = 0
        awake = False
        cv2.putText(img, "[+]Sleepy ratio: {:.3f}".format(ratio), (20, 40), 6, 0.7, (0, 255, 255), 2)

# print("[+]Intializing.....")
det = dlib.get_frontal_face_detector()
pre = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
# print("[+]Intialization complete!")
live_feed = ispy().run()
time.sleep(1.5)  # Camera to load

while True:
    img = live_feed.next()
    # red =  cv2.resize(img, , interpolation=3)  # Resize to speedup and increase accurecy (Interpolation area)
    gscale =  cv2.cvtColor(img, 6)
    faces = det(gscale, 0)
    for face in faces:
        marks = pre(gscale, face)
        marks = npa(marks)
        left_eye = marks[36:42]
        right_eye = marks[42:48]
        left_ratio = open_ratio(left_eye)
        right_ratio = open_ratio(right_eye)
        avg_ratio = (left_ratio + right_ratio) / 2.0  # Better estimation (not winking or other false positives)
        left_hull = cv2.convexHull(left_eye)  # Use convex hull to make sure the all points are taken into consideration, better than bounding rectangle
        right_hull = cv2.convexHull(right_eye)
        cv2.drawContours(img, [left_hull], -1, (0, 255, 255), 1)
        cv2.drawContours(img, [right_hull], -1, (0, 255, 255), 1)
        sleepy(avg_ratio, img)
    cv2.imshow("Camera", img)
    if cv2.waitKey(1) == 27 & 0xFF:
        break
cv2.destroyAllWindows()
live_feed.kill()

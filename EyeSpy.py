import cv2
from threading import Thread
from multiprocessing import Process

class EyeSpy:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)  # Capture from camera at location 0
        self.ret, self.img = self.cap.read()
        self.released = False

    def run(self):
        thread = Thread(target=self.refresh, args=())
        thread.daemon = True
        thread.start()
        return self

    def refresh(self):
        while True:
            if self.released:
                return 0
            self.ret, self.img = self.cap.read()

    def kill(self):
        self.released = True
        self.cap.release()
        # cv2.VideoCapture(0).release()

    def next(self):
        return self.img

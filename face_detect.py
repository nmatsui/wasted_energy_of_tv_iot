#! /usr/bin/env python

import cv2
import sys

from lib import ConsulWrapper as cw
from lib import LEDWrapper as lw

LED_PIN = 8


class FaceDetector(object):
    SCALE_FACTOR = 1.1
    MIN_NEIGHBORS = 5
    MIN_SIZE = (20, 20)

    def __init__(self, cascade_file_name):
        self.led = lw.LEDWrapper(LED_PIN)
        self.consul = cw.ConsulWrapper()
        self.faceClassifier = cv2.CascadeClassifier(cascade_file_name)
        self.led.off()

    def __del__(self):
        self.led.off()

    def detect(self):
        while True:
            video = cv2.VideoCapture(0)
            ret, frame = video.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.faceClassifier.detectMultiScale(
                gray,
                scaleFactor=FaceDetector.SCALE_FACTOR,
                minNeighbors=FaceDetector.MIN_NEIGHBORS,
                minSize=FaceDetector.MIN_SIZE
            )
            self.__notify_detect(len(faces))
            video.release()

    def __notify_detect(self, num_of_faces):
#        print "%d face(s) detected" % num_of_faces
        if num_of_faces == 0:
            self.led.off()
            self.consul.kv_put(cw.ConsulWrapper.FACEDETECT_KEY, False)
        else:
            self.led.on()
            self.consul.kv_put(cw.ConsulWrapper.FACEDETECT_KEY, True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s cascade_file_name" % sys.argv[0]
        sys.exit()

    try:
        print "face_detect start"
        FaceDetector(sys.argv[1]).detect()
    except KeyboardInterrupt as err:
        print "face_detect end"

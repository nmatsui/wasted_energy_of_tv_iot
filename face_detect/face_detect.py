#! /usr/bin/env python

import cv2
import mraa
import sys

PIN = 8

class FaceDetector(object):
    SCALE_FACTOR = 1.1
    MIN_NEIGHBORS = 5
    MIN_SIZE = (20, 20)

    def __init__(self, cascade_file_name):
        self.led = mraa.Gpio(PIN)
        self.led.dir(mraa.DIR_OUT)
        self.led.write(0) 

        self.faceClassifier = cv2.CascadeClassifier(cascade_file_name)

    def __del__(self):
        self.led.write(0)

    def detect(self):
        while True:
            video = cv2.VideoCapture(0)
            ret, frame = video.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.faceClassifier.detectMultiScale(
                gray,
                scaleFactor = FaceDetector.SCALE_FACTOR,
                minNeighbors = FaceDetector.MIN_NEIGHBORS,
                minSize = FaceDetector.MIN_SIZE
            )
            self.__notify_detect(len(faces))
            video.release()

    def __notify_detect(self, num_of_faces):
        print "%d face(s) detected" % num_of_faces
        if num_of_faces == 0:
            self.led.write(0)
        else:
            self.led.write(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s cascade_file_name" % sys.argv[0]
        sys.exit()

    try:
        print "face_detect start"
        FaceDetector(sys.argv[1]).detect()
    except KeyboardInterrupt as err:
        print "face_detect end"

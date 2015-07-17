#! /usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import sys
import time

from datetime import datetime as dt
from lib import BluemixWrapper as bw
from lib import ConsulWrapper as cw

SLEEP = 5


class WatchRatePublisher(object):
    TOPIC = "iot-2/evt/status/fmt/json"

    def __init__(self, bluemix):
        self.consul = cw.ConsulWrapper()
        self.bluemix = bluemix

    def check_state(self):
        while True:
            face = self.consul.kv_get(cw.ConsulWrapper.FACEDETECT_KEY)
            power = self.consul.kv_get(cw.ConsulWrapper.POWERDETECT_KEY)

            if self.__isDetected(power):
                msg = self.__make_msg(self.__isDetected(face))
                self.__publish(msg)

            time.sleep(SLEEP)

    def __isDetected(self, v):
        return True if v and v["Value"] == "True" else False

    def __make_msg(self, face_detected):
        now = dt.now().isoformat() + "+09:00"
        v = "1" if face_detected else "-1"
        return "{\"time\":\"" + now + "\", \"val\":" + v + "}"

    def __publish(self, msg):
        # print "power True : %s" % msg
        self.bluemix.publish(WatchRatePublisher.TOPIC, msg)


class NotifySubscriber(object):
    TOPIC = "iot-2/cmd/notify/fmt/json"

    def __init__(self, bluemix):
        self.consul = cw.ConsulWrapper()
        self.bluemix = bluemix

    def notify(self):
        def callback(msg):
            self.consul.ev_fire(cw.ConsulWrapper.POWER_EVENT)
        self.bluemix.notify(NotifySubscriber.TOPIC, callback)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s iotfoundation_conf_file_name" % sys.argv[0]
        sys.exit()

    try:
        print "watch_rate_publish start"
        bluemix = bw.BluemixWrapper(sys.argv[1])
        NotifySubscriber(bluemix).notify()
        bluemix.connect()
        WatchRatePublisher(bluemix).check_state()
    except KeyboardInterrupt as err:
        print "watch_rate_publish end"

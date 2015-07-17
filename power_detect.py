#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time

from lib import ConsulWrapper as cw
from lib import LEDWrapper as lw
from lib import SWWrapper as sw

LED_PIN = 8
SW_ON_PIN = 3
SW_OFF_PIN = 2


class PowerDetector(object):
    def __init__(self):
        self.led = lw.LEDWrapper(LED_PIN)
        self.sw = sw.SWWrapper(SW_ON_PIN, SW_OFF_PIN)
        self.consul = cw.ConsulWrapper()
        self.led.off()

    def __del__(self):
        self.led.off()

    def detect(self):
        while True:
            if self.sw.is_on():
                self.led.on()
                self.consul.kv_put(cw.ConsulWrapper.POWERDETECT_KEY, True)
            
            if self.sw.is_off():
                self.led.off()
                self.consul.kv_put(cw.ConsulWrapper.POWERDETECT_KEY, False)

if __name__ == "__main__":
    try:
        print "power_detect start"
        PowerDetector().detect()
    except KeyboardInterrupt as err:
        print "power_detect end"

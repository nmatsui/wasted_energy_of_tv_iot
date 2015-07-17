#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time

from lib import ConsulWrapper as cw
from lib import LEDWrapper as lw

LED_PIN = 8
EVENT_SEPARATE_SEC = 5


class PowerReceiver(object):
    def __init__(self):
        self.consul = cw.ConsulWrapper()

    def receive(self):
        ct = time.time()
        lt = self.consul.kv_get(cw.ConsulWrapper.LASTPOWERTIME_KEY)
        if (not lt) or (ct - float(lt["Value"]) > EVENT_SEPARATE_SEC):
            led = lw.LEDWrapper(LED_PIN)
            self.consul.kv_put(cw.ConsulWrapper.LASTPOWERTIME_KEY, ct)
            power = self.consul.kv_get(cw.ConsulWrapper.POWERDETECT_KEY)
            if power and power["Value"] == "True":
                led.off()
                self.consul.kv_put(cw.ConsulWrapper.POWERDETECT_KEY, False)
            else:
                led.on()
                self.consul.kv_put(cw.ConsulWrapper.POWERDETECT_KEY, True)

if __name__ == "__main__":
    PowerReceiver().receive()        

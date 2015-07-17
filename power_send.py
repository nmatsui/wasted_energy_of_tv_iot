#! /usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

from lib import ConsulWrapper as cw
from lib import LEDWrapper as lw

LED_PIN = 8
POWER_CMD = "ssh pi@raspi.local -oStrictHostKeyChecking=no 'irsend SEND_ONCE tv power'"

class PowerSender(object):
    def __init__(self):
        self.consul = cw.ConsulWrapper()
        self.led = lw.LEDWrapper(LED_PIN)

    def send(self):
        subprocess.call(POWER_CMD, shell=True)
        power = self.consul.kv_get(cw.ConsulWrapper.POWERDETECT_KEY)
        if power and power["Value"] == "True":                      
            self.led.off()                         
            self.consul.kv_put(cw.ConsulWrapper.POWERDETECT_KEY, False)
        else:                                                          
            self.led.on()                                           
            self.consul.kv_put(cw.ConsulWrapper.POWERDETECT_KEY, True)

if __name__ == "__main__":
    PowerSender().send()

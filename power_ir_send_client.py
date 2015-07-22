#! /usr/bin/env python
# -*- coding: utf-8 -*-

import socket

from lib import const
from lib import ConsulWrapper as cw
from lib import LEDWrapper as lw

LED_PIN = 8


class PowerIRSendClient(object):

    def __init__(self):
        self.consul = cw.ConsulWrapper()
        self.led = lw.LEDWrapper(LED_PIN)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self):
        try:
            self.s.connect((const.IR_SEND_HOST, const.IR_SEND_PORT))
            self.s.send(const.IR_SEND_MSG)
            self.s.close()
            power = self.consul.kv_get(cw.ConsulWrapper.POWERDETECT_KEY)
            if power and power["Value"] == "True":
                self.led.off()
                self.consul.kv_put(cw.ConsulWrapper.POWERDETECT_KEY, False)
            else:
                self.led.on()
                self.consul.kv_put(cw.ConsulWrapper.POWERDETECT_KEY, True)
        except socket.error as e:
            print "error: %s" % e

if __name__ == "__main__":
    PowerIRSendClient().send()

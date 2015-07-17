#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time

from lib import Decoder as decoder
from lib import ConsulWrapper as cw
from lib import IRWrapper as iw
from lib import LEDWrapper as lw
from lib import SWWrapper as sw

IR_PIN = 7
LED_PIN = 8
SW_ON_PIN = 3
SW_OFF_PIN = 2
SPACE_SEC = 1


class PowerDetector(object):
    POWER_BITS = "010000000000010000000001000000001011110010111101"
    FLAME_SPACE = 50

    def __init__(self):
        self.ir = iw.IRWrapper(IR_PIN)
        self.led = lw.LEDWrapper(LED_PIN)
        self.sw = sw.SWWrapper(SW_ON_PIN, SW_OFF_PIN)
        self.consul = cw.ConsulWrapper()
        self.power = False
        self.__reset()

    def detect(self):
        while True:
            sw_on = self.sw.is_on()
            sw_off = self.sw.is_off()
            if sw_on or sw_off:
                self.power = sw_on
                self.__notify_detect()
                continue

            current = self.ir.read()
            self.nt = time.time() * 1000
            if self.last != current:
                self.last = current
                if not self.recv:
                    self.recv = True
                    self.st = time.time() * 1000
                    continue
                self.code.append({"stete": self.last, "len": self.nt - self.st})
                self.st = self.nt
            if self.recv and self.last == 0 and self.nt - self.st > PowerDetector.FLAME_SPACE:
                bits = decoder.KadenkyoDecoder(self.code).decode()
                pressed = self.__check_power(bits)
                if pressed:
                    self.__notify_detect()
                self.__reset()

    def __check_power(self, bits):
        pressed = False
        if bits == PowerDetector.POWER_BITS:
            now = time.time()
            if now - self.last_power_time > SPACE_SEC:
                self.power = not self.power
                self.last_power_time = now
                pressed = True
        return pressed

    def __notify_detect(self):
        print "power button pressed. now %s" % self.power
        if self.power:
            self.led.on()
            self.consul.kv_put(cw.ConsulWrapper.POWERDETECT_KEY, True)
        else:
            self.led.off()
            self.consul.kv_put(cw.ConsulWrapper.POWERDETECT_KEY, False)

    def __reset(self):
        self.recv = False
        self.last = 0
        self.st = 0
        self.nt = 0
        self.code = []
        self.last_power_time = 0

if __name__ == "__main__":
    try:
        print "power_detect start"
        PowerDetector().detect()
    except KeyboardInterrupt as err:
        print "power_detect end"

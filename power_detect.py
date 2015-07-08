#! /usr/bin/env python
# -*- coding: utf-8 -*-

import mraa
import time

from lib import Decoder as decoder
from lib import IRWrapper as iw

IR_PIN = 7
SPACE_SEC = 1

class PowerDetector(object):
    POWER_BITS = "010000000000010000000001000000001011110010111101"
    FLAME_SPACE = 50

    def __init__(self, ir_pin):
        self.ir = iw.IRWrapper(ir_pin)
        self.power = False
        self.__reset()

    def detect(self):
        while True:
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
#                print bits
                pressed = self.__check_power(bits)
                if pressed:
                    self.__notify_detect()
                self.__reset()

    def __check_power(self, bits):
        pressed = False
        if bits == PowerDetector.POWER_BITS:
#            print "power pressed"
            now = time.time()
            if now - self.last_power_time > SPACE_SEC:
                self.power = not self.power
                self.last_power_time  = now
                pressed = True
        return pressed

    def __notify_detect(self):
        print "power button pressed. now %s" % self.power

    def __reset(self):
        self.recv = False
        self.last = 0
        self.st = 0
        self.nt = 0
        self.code = []
        self.last_power_time = time.time()

if __name__ == "__main__":
    try:
        print "power_detect start"
        PowerDetector(IR_PIN).detect()
    except KeyboardInterrupt as err:
        print "power_detect end"

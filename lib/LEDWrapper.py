# -*- conding: utf-8 -*-

import mraa


class LEDWrapper(object):

    def __init__(self, pin):
        self.led = mraa.Gpio(pin)
        self.led.dir(mraa.DIR_OUT)
        self.off()

    def __del__(self):
        self.off()

    def on(self):
        self.led.write(1)

    def off(self):
        self.led.write(0)

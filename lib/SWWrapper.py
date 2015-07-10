# -*- conding: utf-8 -*-

import mraa

class SWWrapper(object):
    def __init__(self, on_pin, off_pin):
        self.on = mraa.Gpio(on_pin)
        self.on.dir(mraa.DIR_IN)
        self.on.mode(mraa.MODE_PULLUP)
        self.off = mraa.Gpio(off_pin)
        self.off.dir(mraa.DIR_IN)
        self.off.mode(mraa.MODE_PULLUP)
 
    def is_on(self):
        return False if self.on.read() else True

    def is_off(self):
        return False if self.off.read() else True

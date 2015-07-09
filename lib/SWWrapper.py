# -*- conding: utf-8 -*-

import mraa

class SWWrapper(object):
    def __init__(self, on_pin, off_pin):
        self.on = mraa.Gpio(on_pin)
        self.on.dir(mraa.DIR_IN)
        self.off = mraa.Gpio(off_pin)
        self.off.dir(mraa.DIR_IN)
 
    def is_on(self):
        return True if self.on.read() else False

    def is_off(self):
        return True if self.off.read() else False

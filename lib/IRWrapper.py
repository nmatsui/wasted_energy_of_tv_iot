# -*- conding: utf-8 -*-

import mraa

class IRWrapper(object):
    def __init__(self, pin):
        self.ir = mraa.Gpio(pin)
        self.ir.dir(mraa.DIR_IN)
 
    def read(self):
        return not self.ir.read()

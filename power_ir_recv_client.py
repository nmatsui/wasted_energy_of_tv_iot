#! /usr/bin/env python
# -*- coding: utf-8 -*-

import socket

from lib import const

class PowerIRRecvClient(object):

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self):
        try:
            self.s.connect((const.IR_RECV_HOST, const.IR_RECV_PORT))
            self.s.send(const.IR_RECV_MSG)
            self.s.close()
        except socket.error as e:
            print "error: %s" % e

if __name__ == "__main__":
    PowerIRRecvClient().send()

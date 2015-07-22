#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
import threading
import SocketServer

from lib import const
from lib import ConsulWrapper as cw
from lib import LEDWrapper as lw
from lib import SWWrapper as sw

EVENT_SEPARATE_SEC = 5

LED_PIN = 8
SW_ON_PIN = 3
SW_OFF_PIN = 2

class PowerIRRecvHandler(SocketServer.StreamRequestHandler):

    def handle(self):
#        print "connected from:", self.client_address
        sent_data = ""
        while True:
            data = self.request.recv(1024)
            if len(data) == 0:
                break
            sent_data += data

        if sent_data == const.IR_RECV_MSG:
            consul = cw.ConsulWrapper()
            ct = time.time()
            lt = consul.kv_get(cw.ConsulWrapper.LASTPOWERTIME_KEY)
            if (not lt) or (ct - float(lt["Value"]) > EVENT_SEPARATE_SEC):
                led = lw.LEDWrapper(LED_PIN)                              
                consul.kv_put(cw.ConsulWrapper.LASTPOWERTIME_KEY, ct)
                power = consul.kv_get(cw.ConsulWrapper.POWERDETECT_KEY)
                if power and power["Value"] == "True":                      
                    led.off()                         
                    consul.kv_put(cw.ConsulWrapper.POWERDETECT_KEY, False)
                else:                                                          
                    led.on()                                           
                    consul.kv_put(cw.ConsulWrapper.POWERDETECT_KEY, True)

        self.request.close()

class PowerSWDetector(object):

    def __init__(self):
        self.led = lw.LEDWrapper(LED_PIN)
        self.sw = sw.SWWrapper(SW_ON_PIN, SW_OFF_PIN)
        self.consul = cw.ConsulWrapper()
        self.led.off()

    def __del__(self):
        self.led.off()

    def detect(self):
        while True:
            if self.sw.is_on():
                self.led.on()
                self.consul.kv_put(cw.ConsulWrapper.POWERDETECT_KEY, True)

            if self.sw.is_off():
                self.led.off()
                self.consul.kv_put(cw.ConsulWrapper.POWERDETECT_KEY, False)

if __name__ == "__main__":
    address = (const.IR_RECV_HOST, const.IR_RECV_PORT)

    try:
        server = SocketServer.ThreadingTCPServer(address, PowerIRRecvHandler)
        print "power_ir_recv_server listening", server.socket.getsockname()
        t = threading.Thread(target=server.serve_forever)
        t.setDaemon(True)
        t.start()
        PowerSWDetector().detect()
    except KeyboardInterrupt as err:
        print "power_detect end"

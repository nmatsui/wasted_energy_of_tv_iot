#! /usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import SocketServer

from lib import const


class PowerIRSendHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        # print "connected from:", self.client_address
        sent_data = ""
        while True:
            data = self.request.recv(1024)
            if len(data) == 0:
                break
            sent_data += data

        if sent_data == const.IR_SEND_MSG:
            subprocess.call(const.IR_SEND_CMD, shell=True)

        self.request.close()

if __name__ == "__main__":
    address = (const.IR_SEND_HOST, const.IR_SEND_PORT)

    try:
        server = SocketServer.ThreadingTCPServer(address, PowerIRSendHandler)
        print "power_ir_send_server listening", server.socket.getsockname()
        server.serve_forever()
    except KeyboardInterrupt as err:
        server.socket.close()
        print "power_ir_send_server stop"

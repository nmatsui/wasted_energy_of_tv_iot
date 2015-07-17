#! /usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

POWER_CMD = "ssh pi@raspi.local -oStrictHostKeyChecking=no 'irsend SEND_ONCE tv power'"

class PowerSender(object):
    def send(self):
        subprocess.call(POWER_CMD, shell=True)

if __name__ == "__main__":
    PowerSender().send()

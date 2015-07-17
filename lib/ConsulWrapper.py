# -*- conding: utf-8 -*-

import consul

class ConsulWrapper(object):
    FACEDETECT_KEY = "face_detected"
    POWERDETECT_KEY = "power_detected"
    POWER_EVENT = "power"

    def __init__(self):
        self.c = consul.Consul()

    def kv_put(self, key, value):
        self.c.kv.put(key, str(value))

    def kv_get(self, key):
        i, v = self.c.kv.get(key)
        return v

    def ev_fire(self, event):
        self.c.event.fire(event)

# -*- conding: utf-8 -*-

import consul

class ConsulWrapper(object):
    FACEDETECT_KEY = "face_detected"

    def __init__(self):
        self.c = consul.Consul()

    def kv_put(self, key, value):
        self.c.kv.put(key, str(value))

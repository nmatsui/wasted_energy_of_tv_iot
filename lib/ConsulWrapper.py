# -*- conding: utf-8 -*-

import consul
import time

from consul.base import ConsulException
from requests.exceptions import ConnectionError

RETRY_MAX = 60
RETRY_WAIT_SEC = 5

class ConsulWrapper(object):
    FACEDETECT_KEY = "face_detected"
    POWERDETECT_KEY = "power_detected"
    LASTPOWERTIME_KEY = "last_power_time"
    POWER_EVENT = "power"

    def __init__(self):
        self.c = consul.Consul()
        self.errcount = 0

    def kv_put(self, key, value):
        def _f():
            return self.c.kv.put(key, str(value))
        self.__retry(_f)        

    def kv_get(self, key):
        def _f():
            return self.c.kv.get(key)
        i, v = self.__retry(_f)
        return v

    def ev_fire(self, event):
        def _f():
            return self.c.event.fire(event)
        self.__retry(_f)

    def __retry(self, f):
        while True:
            try:
                result = f()
            except (ConsulException, ConnectionError) as e:
                self.errcount += 1
                print "exception %s error count %d" % (e, self.errcount)
                if self.errcount < RETRY_MAX:
                    time.sleep(RETRY_WAIT_SEC)
                    continue
                else:
                    raise e
            break
        self.errcount = 0
        return result

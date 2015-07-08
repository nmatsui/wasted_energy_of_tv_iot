# -*- coding: utf-8 -*-

import paho.mqtt.client as paho
import re

CLIENT_NAME_BASE = "d:%s:%s:%s"
URL_BASE = "%s.messaging.internetofthings.ibmcloud.com"
TOPIC = "iot-2/evt/status/fmt/json"
PORT = 1883
USER = "use-token-auth"

class BluemixWrapper(object):
    def __init__(self, conf):
        org, type, id, token = self.__parse_conf(conf)
        client_name = CLIENT_NAME_BASE % (org, type, id)
        url = URL_BASE % org

        self.mqttc = paho.Client(client_name)
        self.mqttc.username_pw_set(USER, token)
        self.mqttc.connect(url, PORT, 60)

    def publish(self, msg):
        self.mqttc.publish(TOPIC, msg)

    def __parse_conf(self, conf):
        def search(r):
            return next(y for y in [r.match(x) for x in confs] if y).group(1)

        rorg = re.compile(r"^org=(.+)$")
        rtype = re.compile(r"^type=(.+)$")
        rid = re.compile(r"^id=(.+)$")
        rtoken = re.compile(r"^auth-token=(.+)$")

        confs = [x.rstrip() for x in list(open(conf, "r"))]
        return (search(rorg), search(rtype), search(rid), search(rtoken))


# -*- coding: utf-8 -*-

BUF = 0.35
L_HIGH = 3.2
L_LOW = 1.6

D_LOW_0 = 0.4
D_LOW_1 = 1.2


class KadenkyoDecoder(object):

    def __init__(self, code):
        self.code = code

    def decode(self):
        if len(self.code) <= 3:
            return "UNKNOWN"

        paired = self.__make_pair(self.code[:-1])

        if not self.__is_valid_format(paired[0]):
            return "UNKNOWN"
        else:
            return "".join(map(str, map(self.__make_bit, paired[1:])))

    def __make_pair(self, code):
        def pair(l):
            for i in xrange(0, len(l), 2):
                yield {"H": l[i]["len"], "L": l[i + 1]["len"]}
        return list(pair(code))

    def __is_valid_format(self, lc):
        h = L_HIGH - BUF <= lc["H"] <= L_HIGH + BUF
        l = L_LOW - BUF <= lc["L"] <= L_LOW + BUF
        return h and l

    def __make_bit(self, dc):
        if D_LOW_0 - BUF <= dc["L"] <= D_LOW_0 + BUF:
            return 0
        elif D_LOW_1 - BUF <= dc["L"] <= D_LOW_1 + BUF:
            return 1
        else:
            return 9

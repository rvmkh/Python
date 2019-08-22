# -*- coding: utf-8 -*-

import re

def parseRNC(cnhost):
    """ parse RNC <-> CNHOST """
    cnhostHash = {
        "172.17.0.37"   :1,
        "172.17.0.101"  :2,
        "172.17.0.165"  :3,
        "172.17.0.229"  :4,
        "172.17.8.37"   :7,
        "172.17.8.101"  :8,
        "172.17.8.165"  :9,
        "172.17.8.229"  :10,
        "172.17.2.37"   :12,
        "172.17.1.36"   :13,
        "172.17.1.164"  :14,
        "172.17.2.36"   :15,
        "172.17.2.164"  :16,
        "172.17.3.36"   :17,
        "172.17.3.164"  :18,
        "172.17.5.36"   :19,
        "172.17.5.164"  :20
    }

    str1 = re.findall(r'^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$', cnhost)
    if str1:
        return cnhostHash.get(cnhost)

    str2 = re.findall(r'^\d{1,2}$', cnhost)
    if str2:
        for key, value in cnhostHash.items():
            if str(value) == cnhost:
                return key

# cnhost = "4"
# cnhost = "172.17.0.229"
# rnc = parseRNC(cnhost)
# print rnc

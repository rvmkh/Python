# -*- coding: utf-8 -*-

import sqlite3
import re
import sys
import parseRNC as prnc

dbPath = '/home/rvm/scripts/Python/ATCA/atca.db'
conn = sqlite3.connect(dbPath)
cursor = conn.cursor()

def modifyBTS(cell, cab, side, *args):
    """ Update BTS """

    mySet = ""
    sql = ""

    for arg in args:

        matchIp = re.findall(r'^(?i)ip=(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$', arg)
        if matchIp:

            if side == 'L' and matchIp[0][1] == '21':
                newOct2 = '23'
            elif side == 'L' and matchIp[0][1] == '25':
                newOct2 = '27'
            elif side == 'R' and matchIp[0][1] == '21':
                newOct2 = '24'
            elif side == 'R' and matchIp[0][1] == '25':
                newOct2 = '28'
            else:
                newOct2 = '0'

            ip = "'{}.{}.{}.{}'".format(matchIp[0][0], newOct2, matchIp[0][2], matchIp[0][3])
            bngate = "'{}.{}.{}.254'".format(matchIp[0][0], newOct2, matchIp[0][2])

            if mySet == "":
                mySet = "ethrIp={}, fixIP={}, bngate={}".format(ip, ip, bngate)
            else:
                mySet = "{}, ethrIp={}, fixIP={}".format(mySet, ip, ip)

        matchMac = re.findall(r'^(?i)(mac=)(\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2})$', arg)
        if matchMac:
            mac = "{}'{}'".format(matchMac[0][0], matchMac[0][1])
            if mySet == "":
                mySet = mac
            else:
                mySet = "{}, {}".format(mySet, mac)

        matchUrc = re.findall(r'^(?i)urc=([13])$', arg)
        if matchUrc:
            urc = matchUrc[0]
            if mySet == "":
                mySet = "puID='{}'".format(urc)
            else:
                mySet = "{}, puID='{}'".format(mySet, urc)

        matchRnc = re.findall(r'^(?i)rnc=(\d{1,2})$', arg)
        if matchRnc:
            rnc = matchRnc[0]
            cnhost = prnc.parseRNC(rnc)                                             # get cnhost by rnc
            if mySet == "":
                mySet = "cnhost='{}', bssa0='{}', bssa1='{}'".format(cnhost, cnhost, cnhost)
            else:
                mySet = "{}, cnhost='{}', bssa0='{}', bssa1='{}'".format(mySet, cnhost, cnhost, cnhost)

    ######## Update CellSite section ##########
    sql1 = """UPDATE cellsite SET {} WHERE {} and {} and side='{}'""".format(mySet, cell, cab, side)
    cursor.execute(sql1)

    ######## Update SUBNETDECLARATION section ##########
    snet = '{}.{}.{}.0'.format(matchIp[0][0], newOct2, matchIp[0][2])

    sql2 = "UPDATE subnet1107 SET snet='{}' WHERE {} and {} and side='{}'".format(snet, cell, cab, side)
    cursor.execute(sql2)

    sql3 = "UPDATE subnet1108 SET snet='{}' WHERE {} and {} and side='{}'".format(snet, cell, cab, side)
    cursor.execute(sql3)

    conn.commit()

    sql = "{}\n{}\n{}\n".format(sql1, sql2, sql3)
    return sql

# print modifyBTS('cell=9999', 'cab=1', side="L", 'ip=8.21.8.8', ...)

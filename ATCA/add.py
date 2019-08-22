# -*- coding: utf-8 -*-

import sys
import re
import sqlite3
import parseRNC as prnc
import ipCalc as ipc

dbPath = '/home/rvm/scripts/Python/ATCA/atca.db'
conn = sqlite3.connect(dbPath)
cursor = conn.cursor()

def insertBTS(cell, cab, rcvIP, mac, urcid, rnc):
    """ insert new BTS to the CellSite and SUBNETDECLARATION sections """

    ins = ""
    ######## Check input Parameters ##########
    matchCell = re.findall(r'(^\d{1,4}$)', cell)
    if not matchCell:                                                           # check Cell format given by user
        print "Error: Mismatch parameter in Cell!\n"
        exit(0)

    matchIP = re.findall(r'^\s*(\d{1,3})\s*\.\s*(\d{1,3})\s*\.\s*(\d{1,3})\s*\.\s*(\d{1,3})\s*$', rcvIP)
    if not matchIP:                                                             # check IP format given by user
        print "Error: Mismatch parameter in rcvIP!\n"
        exit(0)

    matchMAC = re.findall(r'(^\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)$', mac)
    if not matchMAC:                                                             # check MAC format given by user
        print "Error: Mismatch parameter in MAC!\n"
        exit(0)

    matchCAB = re.findall(r'(^\d$)', cab)
    if not matchCAB:                                                             # check CAB format given by user
        print "Error: Mismatch parameter in CAB!\n"
        exit(0)

    matchURC = re.findall(r'^(\d)$', urcid)
    if not matchURC:                                                             # check URC_ID format given by user
        print "Error: Mismatch parameter in URC_ID!\n"
        exit(0)

    matchRNC = re.findall(r'^(\d{1,2})$', rnc)
    if not matchRNC:                                                             # check RNC format given by user
        print "Error: Mismatch parameter in RNC!\n"
        exit(0)

    insCellNames = 'cell, cab, side, mac, fixIP, btsId, hostName, ethrIp, bngate, cnmask, pct, cnhost, bssa0, bssa1, puID'
    insNetNames = 'cell, cab, side, snet, netMask, nextServ, servName, bssaPortNum, bnmask'

    for side in ['L','R']:                                                      # Transform IP (RCV) depending from Side and 21/25
        ip = ipc.ipCalc(rcvIP, side)
        oct1, newOct2, oct3, oct4 = ip
        ip = '{}.{}.{}.{}'.format(oct1, newOct2, oct3, oct4)

        bngate = "{}.{}.{}.254".format(oct1, newOct2, oct3)
        cnmask = '26'                                                           # Constant
        pct = '4'                                                               # Constant
        cnhost = prnc.parseRNC(rnc)                                             # get cnhost by rnc
        bssa0 = bssa1 = cnhost

        ######## Generate CellSite section ##########
        insCellValues = '"{}", "{}", "{}", "{}", "{}", "{}", "{}cell{}-{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}"'. \
        format(cell, cab, side, mac, ip, cell, side.lower() ,cell, cab, ip, bngate, cnmask, pct, cnhost, bssa0, bssa1, urcid)
        insert_string = 'insert into cellsite ({}) values ({})'. \
        format(insCellNames, insCellValues);
        cursor.execute(insert_string)

        ######## Generate SUBNETDECLARATION section ##########
        snet = '{}.{}.{}.0'.format(oct1, newOct2, oct3)
        insNetValues7 = '"{}", "{}", "{}", "{}", "255.255.255.0", "172.17.0.1", "flx1107-rn", "7900", "24"' . \
        format(cell, cab, side, snet)
        insert_string7 = 'insert into subnet1107 ({}) values ({})'. \
        format(insNetNames, insNetValues7);
        cursor.execute(insert_string7)

        insNetValues8 = '"{}", "{}", "{}", "{}", "255.255.255.0", "172.17.0.2", "flx1108-rn", "7900", "24"' . \
        format(cell, cab, side, snet)
        insert_string8 = 'insert into subnet1108 ({}) values ({})'. \
        format(insNetNames, insNetValues8);
        cursor.execute(insert_string8)

        conn.commit()

    ins = "{}\n{}\n{}".format(insert_string, insert_string7, insert_string8)
    return ins

    cursor.close()
    conn.close()


# insertBTS('6666', '6.25.6.6', '66:66:66:66:66:66', '1', '3', '10')

# -*- coding: utf-8 -*-

import sys
import re

import showAtca as show
import add as add
import makeAtcaLogs as makeLog
import printDhcpd as dhcpd
import modify as mod
#import checkDouble as chkDbl

if sys.argv[1] == "-h":
    print "Usage:"
    # python atca.py add cell='6666' ip='6.21.6.6' mac='66:66:66:66:66:66' cab='1' urc=3 rnc='10'   ## ADD

elif sys.argv[1] == "show":
    cell = sys.argv[2]
    print show.info(cell)

elif sys.argv[1] == "add":                                                      # Create new BTS using user's parameters

    for arg in sys.argv:                                                     # For ADD all parameters are mandatory and can be put in any order

        match = re.findall(r'^(?i)cell=(\d{1,4})$', arg)
        if match:
            cell = match[0]
        match = re.findall(r'^(?i)ip=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$', arg)
        if match:
            ip = match[0]
        match = re.findall(r'^(?i)mac=(\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2})$', arg)
        if match:
            mac = match[0]
        match = re.findall(r'^(?i)cab=([1234])$', arg)
        if match:
            cab = match[0]
        match = re.findall(r'^(?i)urc=([13])$', arg)
        if match:
            urc = match[0]
        match = re.findall(r'^(?i)rnc=(\d{1,2})$', arg)
        if match:
            rnc = match[0]

#    chkDbl.checkDouble(cell, cab, ip, mac)                                      # Checking for doublicating of Cell-Cab, IP or MAC
    try:
        newBTS = add.insertBTS(cell, cab, ip, mac, urc, rnc)                    # Insert new BTS to the Model
        makeLog.makeLogs(cell, "Add", newBTS)                                   # Make Logs
        dhcpd.makeView()                                                        # Generate dhcpd.conf for FLX1107/8
        print "Info: BTS {} created succesfully".format(cell)
    except IndexError:                                                          # Exception if wrong params qtty
        print "Error: Please check input Parameters!\n"

elif sys.argv[1] == "mod":                                                      # Update existing BTS using user parameters
    args = []                                                                   # Updated parameters: Mandatory cell and cab; RANDOM ip, mac, urc, rnc
    for updArg in sys.argv:

        matchCell = re.findall(r'^(?i)(cell=\d{1,4})$', updArg)
        if matchCell:
            cell = matchCell[0]

        matchCab = re.findall(r'^(?i)(cab=[1234])$', updArg)
        if matchCab:
            cab = matchCab[0]

        matchIp = re.findall(r'^(?i)(ip=\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$', updArg)
        if matchIp:
            ip = matchIp[0]
            args.append(ip)

        matchMac = re.findall(r'^(?i)(mac=\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2})$', updArg)
        if matchMac:
            mac = matchMac[0]
            args.append(mac)

        matchUrc = re.findall(r'^(?i)(urc=[13])$', updArg)
        if matchUrc:
            urc = matchUrc[0]
            args.append(urc)

        matchRnc = re.findall(r'^(?i)(rnc=\d{1,2})$', updArg)
        if matchRnc:
            rnc = matchRnc[0]
            args.append(rnc)

    # chkDbl.checkDouble(cell, cab, ip, mac)                                      # Checking for doublicating of Cell-Cab, IP or MAC

    if args and cell and cab:
        lMod = mod.modifyBTS(cell, cab, "L", *args)
        rMod = mod.modifyBTS(cell, cab, "R", *args)
        modRes = "{}\n{}".format(lMod, rMod)

        makeLog.makeLogs(cell, "Modify", modRes)                                                                                 # Make Logs
        dhcpd.makeView()                                                                                                        # Generate
        print "Info: BTS {} updated succesfully\n".format(cell)
    else:
        print "Error: Not enougth params for update!\n"

# elif sys.argv[1] == "del":
#     for arg in sys.argv:                                                     # All parameters are FIXED and mandatory
#         cell = re.findall(r'^(?i)cell=(\d{1,4})$', arg)
#         if cell:
#             paramArr.insert(0, cell)
#         cab = re.findall(r'^(?i)cab=([1234])$', arg)
#         if cab:
#             paramArr.insert(3, cab)

else:
    print "Please type -h"

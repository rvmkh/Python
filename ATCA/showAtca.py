# -*- coding: utf-8 -*-

import sqlite3
import parseRNC as prnc

conn = sqlite3.connect('/home/rvm/scripts/Python/ATCA/atca.db')
c = conn.cursor()

def info(cell):
    """ Print cell info """

    print "Cell\tCab\tMAC\t\t\tFIX_IP\t\tRNC"
    cabs = [1,2,3,4]
    for i in cabs:
        c.execute('select cell, cab, mac, fixIP, cnhost from cellsite where cell=' + cell + ' and cab=' + str(i) + ' and side="L"')
        query = c.fetchone()
        if query:
            cell = query[0]
            cab = query[1]
            mac = query[2]
            fixIP = query[3]
            cnhost = query[4]
            rnc = prnc.parseRNC(cnhost)
            queryRes = cell + "\t" + cab + "\t" + mac + "\t" + fixIP + "\t" + str(rnc)
            return queryRes
    c.close()
    conn.close()

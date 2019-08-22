# -*- coding: utf-8 -*-

import subprocess
import sqlite3
import re

dbPath = '/home/rvm/scripts/Python/ATCA/atca.db'
conn = sqlite3.connect(dbPath)
cursor = conn.cursor()

def printSubnet(flxNum):
    """ make Subnet List for FLX110* """
    flx = []
    query_string = 'select cell, cab, side, snet, netMask, nextServ, servName, bssaPortNum, bnmask' \
    ' from subnet110{}'.format(flxNum)
    cursor.execute(query_string)
    query = cursor.fetchall()                                                                   # get all queries

    if query:
        for i in query:                                                                         # get each query
            cell_num, cab, side, snet, netMask, nextServ, servName, bssaPortNum, bnmask = i     # unpack Tuple to vars ( i == select result )
            flx.append('SUBNET-{}-BEGIN\n'.format(snet))
            flx.append('subnet {} netmask {}\n'.format(snet, netMask))
            flx.append('{\n')
            flx.append('\tnext-server {};\n'.format(nextServ))
            flx.append('\tserver-name {};\n'.format(servName))
            flx.append('\toption urc1.bssaPortNum {};\n'.format(bssaPortNum))
            flx.append('\toption urc1.bnmask {};\n'.format(bnmask))
            flx.append('\t#HOST {}CELL{}-{}-ATTACHED;\n'.format(side, cell_num, cab))
            flx.append('}\n')
            flx.append('SUBNET-{}-END\n'.format(snet))

        return flx

def printCellsite():
    """ make CellSite List for FLX110* """
    cellSite = []
    query_string = 'select cell, cab, side, mac, fixIP, btsId, hostName, ethrIp, bngate, cnmask, pct, cnhost, bssa0, bssa1, puID from cellsite'
    cursor.execute(query_string)
    query = cursor.fetchall()                                                                                             # get all queries

    if query:
        for i in query:                                                                                                   # get each query
            cell, cab, side, mac, fixIP, btsId, hostName, ethrIp, bngate, cnmask, pct, cnhost, bssa0, bssa1, puID = i     # unpack Tuple to vars ( i == select result )

            cellSite.append('group CELLSITE\n')
            cellSite.append('{\n')
            cellSite.append('#CELL{}-{}-BEGIN\n'.format(cell, cab))
            cellSite.append('\thost {}CELL{}-{}\n'.format(side, cell, cab))
            cellSite.append('\t{\n')
            cellSite.append('\toption dhcp-client-identifier {};\n'.format(mac))
            cellSite.append('\tfixed-address {};\n'.format(fixIP))
            cellSite.append('\toption host-name "{}cell{}-{}";\n'.format(side.lower(), cell, cab))
            cellSite.append('\toption urc1.ethrIp {};\n'.format(ethrIp))
            cellSite.append('\toption urc1.bngate {};\n'.format(bngate))
            cellSite.append('\toption urc1.cnmask {};\n'.format(cnmask))
            cellSite.append('\toption urc1.ParentCabType {};\n'.format(pct))
            if puID == '1':
                cellSite.append('\toption urc1.ParentUrcId {};\n'.format(puID))
            cellSite.append('\toption urc1.cnhost {};\n'.format(cnhost))
            cellSite.append('\toption urc1.bssaipaddr0 {};\n'.format(bssa0))
            cellSite.append('\toption urc1.bssaipaddr0 {};\n'.format(bssa1))
            cellSite.append('\t}\n')
            cellSite.append('#CELL{}-{}-END\n'.format(cell, cab))
            cellSite.append('}\n')

        return cellSite

def calcCksum(flxNum):
    """ calculate cksum of dhcpd-file """
    getCksum = subprocess.check_output(['cksum', './dhcpdRes/dhcpd_110{}.conf'.format(flxNum)])
    match = re.findall(r'(\d+)\s+\d+', getCksum)
    if match:
        cksum = match[0]
    else:
        cksum = "Error: Cannot calculate cksum for FLX110{}!\n".format(flxNum)
    return cksum

def makeView():
    """ Print DHCPD.conf for FLX1107/8 """

    netHeader7 = open('./headerFooter/1107_netHeader.conf', 'r')
    netFooter = open('./headerFooter/netFooter.conf', 'r')
    cellHeader = open('./headerFooter/cellHeader.conf', 'r')
    cellFooter = open('./headerFooter/cellFooter.conf', 'r')
    with open('./dhcpdRes/dhcpd_1107.conf', 'w') as dhcpd7:
        dhcpd7.write(''.join(netHeader7))
        dhcpd7.write(''.join(printSubnet("7")))
        dhcpd7.write(''.join(netFooter))
        dhcpd7.write(''.join(cellHeader))
        dhcpd7.write(''.join(printCellsite()))
        dhcpd7.write(''.join(cellFooter))
        dhcpd7.write(''.join('#cksumDhcpAtca:{}\n'.format(calcCksum("7"))))
    dhcpd7.close()
    netHeader7.close()
    netFooter.close()
    cellHeader.close()
    cellFooter.close()

    netHeader8 = open('./headerFooter/1108_netHeader.conf', 'r')
    netFooter = open('./headerFooter/netFooter.conf', 'r')
    cellHeader = open('./headerFooter/cellHeader.conf', 'r')
    cellFooter = open('./headerFooter/cellFooter.conf', 'r')
    with open('./dhcpdRes/dhcpd_1108.conf', 'w') as dhcpd8:
        dhcpd8.write(''.join(netHeader8))
        dhcpd8.write(''.join(printSubnet("8")))
        dhcpd8.write(''.join(netFooter))
        dhcpd8.write(''.join(cellHeader))
        dhcpd8.write(''.join(printCellsite()))
        dhcpd8.write(''.join(cellFooter))
        dhcpd8.write(''.join('#cksumDhcpAtca:{}\n'.format(calcCksum("8"))))
    dhcpd8.close()
    netHeader8.close()
    netFooter.close()
    cellHeader.close()
    cellFooter.close()

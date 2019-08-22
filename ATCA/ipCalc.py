# -*- coding: utf-8 -*-

import re

def ipCalc(rcvIP, side):
    """ reCalc rcvIP to fixIP """

    matchIP = re.findall(r'^\s*(\d{1,3})\s*\.\s*(\d{1,3})\s*\.\s*(\d{1,3})\s*\.\s*(\d{1,3})\s*$', rcvIP)
    oct1, oct2, oct3, oct4 = matchIP[0]

    if side == 'L' and oct2 == '21':
        newOct2 = '23'
    elif side == 'L' and oct2 == '25':
        newOct2 = '27'
    elif side == 'R' and oct2 == '21':
        newOct2 = '24'
    elif side == 'R' and oct2 == '25':
        newOct2 = '28'
    else:
        newOct2 = '0'

    return (oct1, newOct2, oct3, oct4)


# print ipCalc('172.21 .1  .20', 'L')

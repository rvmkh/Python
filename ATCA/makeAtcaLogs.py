# -*- coding: utf-8 -*-
from datetime import datetime, date, time

def makeLogs(cell, action, sql):
    """ make atca logs """
    with open('./LOG/atca.log', 'a') as logs:
        logs.write(''.join('{} Cell {} action {}\n{}\n'.format(datetime.today(), cell, action, sql)))
    logs.close()

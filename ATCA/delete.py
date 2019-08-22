# -*- coding: utf-8 -*-

import sqlite3

dbPath = '/home/rvm/scripts/Python/ATCA/atca.db'
conn = sqlite3.connect(dbPath)
cursor = conn.cursor()

def deleteBTS(cell, cab):
    """ Delete BTS """

    sql = ""
    ######## Delete CellSite section ##########
    sql1 = """DELETE from cellsite WHERE cell='{}' and cab='{}'""".format(cell, cab)
    cursor.execute(sql1)

    ######## Delete SUBNETDECLARATION section ##########
    sql2 = "DELETE from subnet1107 WHERE cell='{}' and cab='{}'""".format(cell, cab)
    cursor.execute(sql2)

    sql3 = "DELETE from subnet1108 WHERE cell='{}' and cab='{}'""".format(cell, cab)
    cursor.execute(sql3)

    conn.commit()
    sql = "{}\n{}\n{}\n".format(sql1, sql2, sql3)
    return sql

# print deleteBTS(7777, 1)

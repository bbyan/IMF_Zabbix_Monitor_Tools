# !/usr/bin/python
# -*- coding:UTF-8 -*-
"""
Author: Lu Bin
Contact:blu@cm-topsci.com
"""
import cx_Oracle
import sys
import ConfigParser


def import_config(path):
    # Initialize the external configuration file
    cf = ConfigParser.ConfigParser()
    cf.read(path)
    # AIMS Server configuration
    i_aims_master_server = cf.get("databaseServer", sys.argv[1])
    i_query_statement = cf.get("query", sys.argv[2])
    return i_aims_master_server, i_query_statement


# The oracle query common structure
def oracle_query(host, query):
    conn = cx_Oracle.connect(host)
    cursor = conn.cursor()
    cursor.execute(query)
    count = cursor.fetchall()[0][0]
    cursor.close()
    conn.close()
    return count


if __name__ == "__main__":
    aims_master_server, query_statement = import_config("./query.conf")
    query_return = oracle_query(aims_master_server, query_statement)
    print query_return

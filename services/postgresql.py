#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = 'Javier Aguila <javier@kliento.mx>'
__copyright__ = ''
__license__   = ''

import psycopg2

def plugin(srv, item):
    srv.logging.debug("*** MODULE=%s: service=%s, target=%s", __file__, item.service, item.target)

    host     = item.config.get('host', 'localhost')
    port     = item.config.get('port', 5432)
    user     = item.config.get('user')
    password = item.config.get('password')
    dbname   = item.config.get('database')

    if user == None:
        srv.logging.warn("You must specify the user for connect to PostgreSQL")
        return False

    if password == None:
        srv.logging.warn("You must specify the user password for connect to PostgreSQL")
        return False

    if dbname == None:
        srv.logging.warn("You must specify the database name to connect to PostgreSQL")
        return False

    try:
        table_name = item.addrs[0].format(**item.data).encode('utf-8')
        fallback_col = item.addrs[1].format(**item.data).encode('utf-8')
    except:
        srv.logging.warn("PostgreSQL target incorrectly configured")
        return False

    return True
    # try:
    #     connection = psycopg2.connect(host = host,
    #         port = port,
    #         user = user,
    #         password = password,
    #         database = database)
    #     cursor = connection.cursor()
    # except Exception e:
    #     srv.logging.warn("Cannot connect to PostgreSQL: %s" % (str(e)))

    # text = item.message

    # srv.logging.debug("#####")
    # srv.logging.debug(cursor)
    # srv.logging.debug("#####")
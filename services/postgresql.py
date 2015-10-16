#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = 'Javier Aguila <javier@kliento.mx>'
__copyright__ = ''
__license__   = ''

import psycopg2

def add_row(cursor, table_name, rowdict):
    unknown_keys = None

    # Filter out keys that are not columnn names
    cursor.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '%s'" % table_name)
    allowed_keys = set(row[0] for row in cursor.fetchall())
    keys = allowed_keys.intersection(rowdict)

    if len(rowdict) > len(keys):
        unknown_keys = set(rowdict) - allowed_keys

    columns = ", ".join(keys)
    values_template = ", ".join(["%s"] * len(keys))

    sql = "INSERT INTO %s (%s) values (%s)" % (table_name, columns, values_template)
    values = tuple(rowdict[key] for key in keys)
    cursor.execute(sql, values)

    return unknown_keys

def plugin(srv, item):
    srv.logging.debug("*** MODULE=%s: service=%s, target=%s", __file__, item.service, item.target)

    host     = item.config.get('host', 'localhost')
    port     = item.config.get('port', 5432)
    user     = item.config.get('user')
    password = item.config.get('password')
    database = item.config.get('database')

    if user == None:
        srv.logging.warn("You must specify the user for connect to PostgreSQL")
        return False

    if password == None:
        srv.logging.warn("You must specify the user's password for connect to PostgreSQL")
        return Falseadd_row

    if database == None:
        srv.logging.warn("You must specify the database name to connect to PostgreSQL")
        return False

    try:
        table_name = item.addrs[0].format(**item.data).encode('utf-8')
        fallback_col = item.addrs[1].format(**item.data).encode('utf-8')
    except:
        srv.logging.warn("PostgreSQL target incorrectly configured")
        return False

    try:
        connection = psycopg2.connect(host = host,
            port = port,
            user = user,
            password = password,
            database = database)
        cursor = connection.cursor()
    except Exception, e:
        srv.logging.warn("Cannot connect to PostgreSQL: %s" % (str(e)))

    text = item.message

    # Create new dict for column data. First add fallback column
    # with full payload. Then attempt to use formatted JSON values
    col_data = {
        fallback_col : text
    }

    if item.data is not None:
        for key in item.data.keys():
            try:
                col_data[key] = item.data[key].format(**item.data).encode('utf-8')
            except Exception, e:
                col_data[key] = item.data[key]

    try:
        unknown_keys = add_row(cursor, table_name, col_data)
        if unknown_keys is not None:
            srv.logging.debug("Skipping unused keys %s" %",".join(unknown_keys))
        connection.commit()
    except Exception, e:
        srv.logging.warn("Cannot add PostgreSQL row: %s" % (str(e)))
        cursor.close()
        connection.close()
        return False

    cursor.close()
    connection.close()

    return True
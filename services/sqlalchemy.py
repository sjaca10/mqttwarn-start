#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine

__author__    = 'Javier Aguila <sjaca10@gmail.com>'
__copyright__ = ''
__license__   = ''

def is_validate_item(item):
    if item == None:
        return False
    return True

def plugin(srv, item):
    srv.logging.debug("*** MODULE=%s: service:%s, target=%s", __file__, item.service, item.target)

    hosts     = item.config.get('hosts', 'localhost')
    drivers   = item.config.get('drivers')
    dialects  = item.config.get('dialects')
    ports     = item.config.get('ports')
    users     = item.config.get('users')
    passwords = item.config.get('passwords')
    databases = item.config.get('databases')

    if (is_validate_item(dialects) and is_validate_item(drivers) and is_validate_item(ports) and
        is_validate_item(users) and is_validate_item(passwords) and is_validate_item(databases)):
        srv.logging.warn("Bad configuration on SQLAlchemy")
        return False

    # Create list of engines to connect to different DBMS
    for i in range(len(dialects)):
        connection_string = dialects[i] + "+" + drivers[i] + '://'

        if len(users) == 1:
            connection_string += users[0]
        else:
            connection_string += users[i]
        connection_string += ":"

        if len(passwords) == 1:
            connection_string += users[0]
        else:
            connection_string += users[i]
        connection_string += "@"

        if len(hosts) == 1:
            connection_string += hosts[0]
        else:
            connection_string += hosts[i]
        connection_string += ":"

        if len(ports) == 1:
            connection_string += str(ports[0])
        else:
            connection_string += str(ports[i])
        connection_string += "/"

        if len(databases) == 1:
            connection_string += databases[0]
        else:
            connection_string += databases[i]

        srv.logging.debug("Configure connection %s" % connection_string)
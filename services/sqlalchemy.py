#not /usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData

__author__    = 'Javier Aguila <sjaca10@gmail.com>'
__copyright__ = ''
__license__   = ''

def is_valid(item):
    if item == None:
        return False
    return True

def plugin(srv, item):
    srv.logging.debug("*** MODULE=%s: service:%s, target=%s", __file__, item.service, item.target)

    # Get information from ini configuration file
    hosts     = item.config.get('hosts', 'localhost')
    drivers   = item.config.get('drivers')
    dialects  = item.config.get('dialects')
    ports     = item.config.get('ports')
    users     = item.config.get('users')
    passwords = item.config.get('passwords')
    databases = item.config.get('databases')

    # Validate the configuration information is set up
    if (not is_valid(dialects) or not is_valid(drivers) or not is_valid(ports) or not is_valid(users) or not is_valid(passwords) or not is_valid(databases)):
        srv.logging.warn("Bad configuration, review the required information")
        return False

    try:
        dialect_target   = item.addrs[0].format(**item.data).encode('utf-8')
        operation_target = item.addrs[1].format(**item.data).encode('utf-8')
        tables_target    = item.addrs[2].format(**item.data).encode('utf-8')
        print "##############"
        print dialect_target
        print operation_target
        print tables_target
        print "##############"
    except Exception, e:
        srv.logging.warn("Target incorrectly configured")
        return False

    # Set up the data structure to store the base maps from SQLAlchemy
    (metadata, bases, engines) = (dict(), dict(), dict())

    for i in range(len(dialects)):
        connection_string = dialects[i] + '+' \
        + drivers[i] + '://' \
        + users     [(0, i)[len(users)      > 1]]   + ':' \
        + passwords [(0, i)[len(passwords)  > 1]]   + '@' \
        + hosts     [(0, i)[len(hosts)      > 1]]   + ':' \
        + str(ports [(0, i)[len(ports)      > 1]])  + '/' \
        + databases [(0, i)[len(databases)  > 1]]

        srv.logging.debug("Configure connection %s" % connection_string)

        # Create dict of engines to connect to different DBMS
        engines[dialects[i]] = create_engine(connection_string)

        # Produce our own metadata object
        metadata[dialects[i]] = MetaData()

        # Reflect from database limiting what tables we look at
        metadata[dialects[i]].reflect(engines[dialects[i]], only = [tables_target])

        # Create dict of introspection Base class to reverse engineering
        bases[dialects[i]] = automap_base(metadata = metadata[dialects[i]])

        # Reflecting the databases from engines
        bases[dialects[i]].prepare()

    for key in bases:
        print "For " + key + " mapping: "
        for value in bases[key].classes:
            print value

    return True
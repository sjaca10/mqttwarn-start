#not /usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = 'Javier Aguila <sjaca10@gmail.com>'
__copyright__ = ''
__license__   = ''

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, MetaData
import paho.mqtt.client as mqtt
import json

def is_valid(item):
    if item == None:
        return False
    return True

def create(srv, session, tables, data):
    try:
        for t in tables:
            if t in data:
                map_object = tables[t]
                session.add(map_object(**data[t]))
                session.commit()
            else:
                srv.logging.debug("No data for %s", t)
    except Exception, e:
        srv.logging.warn("Error store mapped objects")
        srv.logging.debug(e)

# TODO: Add support to multiple query tables at the same publish
# TODO: Optimaze when add more filters
def read(srv, session, tables, data):
    for t in tables:
        if t in data:
            if data[t]["filter"] == "equals":
                query_results = session.query(tables[t]).filter(getattr(tables[t],
                    data[t]["column"]) == data[t]["value"])

                objects = []
                for r in query_results:
                    objects.append(r.__dict__)
                payload_result, payload_result["results"] = (dict(), dict())
                payload_result["results"][t] = objects

                client = mqtt.Client()
                client.connect("localhost", 1883, 60)
                client.publish("results", payload = str(payload_result))
                client.disconnect()
            else:
                srv.logging.warn("Filter not supported")

# TODO: Add suppor to multiple update tables at the same publish
# TODO: Optimaze when add more filters
# TODO: Analyze and implement cascade update
def update(srv, session, tables, data):
    for t in tables:
        if data[t]["filter"] == "equals":
            query_results = session.query(tables[t]).filter(getattr(tables[t],
                data[t]["search"]) == data[t]["value"])

            for r in query_results:
                setattr(r, data[t]["update"], data[t]["new"])

            session.commit()

            client = mqtt.Client()
            client.connect("localhost", 1883, 60)
            client.publish("results", payload = '{"status":"OK"}')
            client.disconnect()
        else:
            srv.logging.warn("Filter not supported")

# TODO: Add support to multiple query tables at the same publish
# TODO: Optimaze when add more filters
# TODO: Analyze and implement cascade elimination
def delete(srv, session, tables, data):
    for t in tables:
        if t in data:
            if data[t]["filter"] == "equals":
                query_results = session.query(tables[t]).filter(getattr(tables[t],
                    data[t]["column"]) == data[t]["value"])

                for r in query_results:
                    session.delete(r)

                session.commit()

                client = mqtt.Client()
                client.connect("localhost", 1883, 60)
                client.publish("results", payload = '{"status":"OK"}')
                client.disconnect()
            else:
                srv.logging.warn("Filter not supported")

def plugin(srv, item):
    srv.logging.debug("*** MODULE=%s: service:%s, target=%s", __file__, item.service, item.target)

    # Get information from ini configuration file
    hosts     = item.config.get('hosts', 'localhost')
    jsondata  = item.config.get('jsondata', 'data')
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

    # Get the information required to interact with database
    try:
        dialect_target   = item.addrs[0].format(**item.data).encode('utf-8')
        operation_target = item.addrs[1].format(**item.data).encode('utf-8')
        tables_target    = item.addrs[2].format(**item.data).encode('utf-8').split(",")
    except Exception, e:
        srv.logging.warn("Target incorrectly configured")
        srv.logging.debug(e)
        return False

    # Creating the string to connect with DBMS trough SQLAlchemy
    if dialect_target in dialects:
        dialect_index = dialects.index(dialect_target)
        connection_string = dialects[dialect_index] + '+' \
        + drivers[dialect_index] + '://' \
        + users     [(0, dialect_index)[len(users)      > 1]]   + ':' \
        + passwords [(0, dialect_index)[len(passwords)  > 1]]   + '@' \
        + hosts     [(0, dialect_index)[len(hosts)      > 1]]   + ':' \
        + str(ports [(0, dialect_index)[len(ports)      > 1]])  + '/' \
        + databases [(0, dialect_index)[len(databases)  > 1]]

        srv.logging.debug("Configure connection %s" % connection_string)
    else:
        srv.logging.warn("Dialect target not found in dialects configuration")

        srv.logging.warn
    # Database introspection generating mappings from an existing metaData
    try:
        # Create dict of engines to connect to different DBMS
        engine = create_engine(connection_string)

        # Produce our own metadata object
        metadata = MetaData()

        # Reflect from database limiting what tables we look at
        metadata.reflect(engine, only = tables_target)

        # Create dict of introspection Base class to reverse engineering
        base = automap_base(metadata = metadata)

        # Reflecting the databases from engine
        base.prepare()

    except Exception, e:
        srv.logging.warn("The database introspection trough SQLAlchemy failed")
        srv.logging.debug(e)

    # Get the classes getting from the database
    try:
        classes = dict()
        for table in tables_target:
            classes[table] = getattr(base.classes, table)
    except Exception, e:
        srv.logging.warn("Getting the classes resulting from introspection failed")
        srv.logging.debug(e)

    # Associate DB with engine to talk with
    session = Session(engine)

    # Generate dict from JSON payload
    data = item.data[jsondata]

    # Check the desired operation and call the appropriate function
    if operation_target == "c":
        # Create
        create(srv, session, classes, data)
    elif operation_target == "r":
        # Read
        read(srv, session, classes, data)
    elif operation_target == "u":
        # Update
        update(srv, session, classes, data)
    elif operation_target == "d":
        # Delete
        delete(srv, session, classes, data)
    else:
        srv.logging.warn("Operation not supported")

    return True
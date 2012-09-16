#!/usr/bin/env python
"""
This is a trivial example of how to use kismetclient in an application.
"""
from kismetclient import Client as KismetClient
from kismetclient import handlers

from pprint import pprint

import logging
log = logging.getLogger('kismetclient')
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


address = ('127.0.0.1', 2501)
k = KismetClient(address)
k.register_handler('TRACKINFO', handlers.print_fields)


def handle_ssid(client, ssid, mac):
    print 'ssid spotted: "%s" with mac %s' % (ssid, mac)

k.register_handler('SSID', handle_ssid)

try:
    while True:
        k.listen()
except KeyboardInterrupt:
    pprint(k.protocols)
    log.info('Exiting...')

#!/usr/bin/env python
from kismetclient.client import Client as KismetClient
from kismetclient import handlers

from pprint import pprint

import logging
log = logging.getLogger('kismetclient')
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


address = ('127.0.0.1', 2501)
k = KismetClient(address)
k.register_handler('TRACKINFO', handlers.print_fields)

try:
    while True:
        k.listen()
except KeyboardInterrupt:
    pprint(k.protocols)
    print('\nExiting...')

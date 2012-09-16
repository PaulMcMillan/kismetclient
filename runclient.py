from kismetclient.kismet import KismetClient
from kismetclient import handlers

from pprint import pprint

address = ('127.0.0.1', 2501)
k = KismetClient(address)
k.register_handler('TRACKINFO', handlers.print_fields)

try:
    while True:
        k.read()
except KeyboardInterrupt:
    pprint(k.capabilities)
    print('\nExiting...')

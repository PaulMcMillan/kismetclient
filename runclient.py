from kismetclient.kismet import KismetClient
from kismetclient import handlers

#address = ('10.4.0.71', 2501)
address = ('127.0.0.1', 2501)
k = KismetClient(address)
k.register_handler('TRACKINFO', handlers.print_fields)

try:
    while True:
        k.read()
except KeyboardInterrupt:
    print k.capabilities
    print '\nExiting...'

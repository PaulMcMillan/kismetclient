import socket
import re
import subprocess
import logging

from pprint import pprint
from time import sleep

from kismetclient import handlers
from kismetclient.protocol import KismetCommand
from kismetclient.protocol import KismetResponse
from kismetclient.utils import get_csv_args
from kismetclient.utils import get_pos_args

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


class KismetClient(object):
    def __init__(self, address=('localhost', 2501)):
        self.handlers = {}
        self.capabilities = {}
        self.in_progress = {}
        self.register_handler('KISMET',
                              handlers.kismet,
                              send_enable=False)
        self.register_handler('PROTOCOLS',
                              handlers.protocols,
                              send_enable=False)
        self.register_handler('CAPABILITY',
                              handlers.capability,
                              send_enable=False)
        self.register_handler('ACK',
                              handlers.ack,
                              send_enable=False)
        self.register_handler('ERROR',
                              handlers.error,
                              send_enable=False)
        self.file = socket.create_connection(address).makefile('w', 1)
        # Do this better.
        self.read()  # Kismet startup line
        self.read()  # Protocols line triggers capabilities reqs
        while len(self.in_progress) > 0:
            self.read()
        # Capabilities done populating

    def register_handler(self, protocol, handler, send_enable=True):
        """ Register a protocol handler, and (optionally) send enable
        sentence.
        """
        self.handlers[protocol] = handler
        if send_enable:
            fields = get_csv_args(handler)
            if not fields:
                fields = '*'
            self.cmd('ENABLE', protocol, fields)

    def cmd(self, command, *opts):
        cmd = KismetCommand(command, *opts)
        log.debug(cmd)
        self.in_progress[str(cmd.command_id)] = cmd
        self.file.write(cmd)

    def read(self):
        line = self.file.readline().rstrip('\n')
        r = KismetResponse(line)
        handler = self.handlers.get(r.protocol)
        if handler:
            fields = r.fields
            if get_pos_args(handler):
                # just the named parameters in handler
                return handler(self, *fields)
            else:
                # all parameters in default order
                field_names = self.capabilities.get(r.protocol, [])
                # If the protocol fields aren't known at all, we don't
                # handle the message.
                if field_names:
                    named_fields = {k: v for k, v in zip(field_names, fields)}
                    return handler(self, **named_fields)

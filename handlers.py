from inspect import getargspec
from utils import csv

def _pos_args(handler):
    """ Return the names of a handler's positional args """
    return getargspec(handler).args[1:]

def kismet(server, version, starttime, servername, dumpfiles, uid):
    print version, servername

def capability(server, CAPABILITY, capabilities):
    server.capabilities[CAPABILITY] = csv(capabilities)

def protocols(server, protocols):
    for protocol in csv(protocols):
        server.cmd('CAPABILITY', protocol)

def ack(server, cmdid, text):
    server.in_progress.pop(cmdid)

def error(server, cmdid, text):
    cmd = server.in_progress.pop(cmdid)
    # FIXME make a real exception
    raise Exception(str(cmd), text)

def print_fields(server, **fields):
    """ A generic handler which prints all the fields. """
    for k, v in fields.items():
        print '%s: %s' % (k, v)
    print '-' * 80

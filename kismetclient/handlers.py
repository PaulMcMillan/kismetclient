from kismetclient.utils import csv
from kismetclient.exceptions import ServerError


def kismet(server, version, starttime, servername, dumpfiles, uid):
    """ Handle server startup string. """
    print version, servername, uid


def capability(server, CAPABILITY, capabilities):
    """ Register a server's capability. """
    server.capabilities[CAPABILITY] = csv(capabilities)


def protocols(server, protocols):
    """ Enumerate capabilities so they can be registered. """
    for protocol in csv(protocols):
        server.cmd('CAPABILITY', protocol)


def ack(server, cmdid, text):
    """ Handle ack messages in response to commands. """
    # Simply remove from the in_progress queue
    server.in_progress.pop(cmdid)


def error(server, cmdid, text):
    """ Handle error messages in response to commands. """
    cmd = server.in_progress.pop(cmdid)
    raise ServerError(cmd, text)


def print_fields(server, **fields):
    """ A generic handler which prints all the fields. """
    for k, v in fields.items():
        print '%s: %s' % (k, v)
    print '-' * 80

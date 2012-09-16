from kismetclient.utils import csv
from kismetclient.exceptions import ServerError


def kismet(server, version, starttime, servername, dumpfiles, uid):
    print version, servername


def capability(server, CAPABILITY, capabilities):
    server.capabilities[CAPABILITY] = csv(capabilities)


def protocols(server, protocols):
    for protocol in csv(protocols):
        server.cmd('CAPABILITY', protocol)


def ack(server, cmdid, text):
    """ Handle ack messages for commands. """
    server.in_progress.pop(cmdid)


def error(server, cmdid, text):
    """ Handle error messages for commands. """
    cmd = server.in_progress.pop(cmdid)
    raise ServerError(cmd, text)


def print_fields(server, **fields):
    """ A generic handler which prints all the fields. """
    for k, v in fields.items():
        print '%s: %s' % (k, v)
    print '-' * 80

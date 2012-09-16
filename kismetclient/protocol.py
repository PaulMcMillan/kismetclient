import re


class Command(object):
    # assign at the class level, so these are unique.
    # FIXME race condition.
    command_id = 0

    def __init__(self, command, *opts):
        Command.command_id += 1
        self.command_id = Command.command_id
        self.command = command

        def wrap(opt):
            if ' ' in opt:
                return '\x01%s\x01'
            else:
                return opt
        self.opts = map(wrap, opts)

    def __str__(self):
        return '!%d %s %s\n' % (self.command_id,
                                self.command,
                                ' '.join(self.opts))


class Response(object):
    protocol = ''
    fields = []

    def __init__(self, res):
        if not res.startswith('*'):
            raise ValueError('Attempted to create a Response object '
                             'from string which did not start with "*"')
        self.protocol, _, tail = res[1:].partition(':')
        fields = re.findall(' \x01(.*?)\x01| ([^ ]+)', tail)
        # only one of the regex fields will match; the other will be empty
        self.fields = [''.join(f) for f in fields]

    def __str__(self):
        return '*%s: %s' % (self.protocol, str(self.fields))

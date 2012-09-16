import re


class KismetResponse(object):
    protocol = ''
    fields = []
    def __init__(self, res):
        if not res.startswith('*'):
            return None
        self.protocol, _, tail = res[1:].partition(':')
        fields = re.findall(' \x01(.*?)\x01| ([^ ]+)', tail)
        self.fields = [''.join(f) for f in fields]

    def __str__(self):
        return '*%s: %s' % (self.protocol, str(self.fields))


class KismetCommand(object):
    command_id = 0
    def __init__(self, command, *opts):
        # assign at the class level, so these are unique.
        # FIXME race condition.
        KismetCommand.command_id += 1
        self.command_id = KismetCommand.command_id
        self.command = command
        def wrap(opt):
            if ' ' in opt:
                return '\x01%s\x01'
            else:
                return opt
        self.opts = [wrap(opt) for opt in opts]

    def __str__(self):
        return '!%d %s %s\n' % (self.command_id,
                                self.command,
                                ' '.join(self.opts))


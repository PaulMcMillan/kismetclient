def csv(val):
    if isinstance(val, basestring):
        return val.split(',')
    elif hasattr(val, '__iter__'):
        return ','.join(map(str, val))
    else:
        raise Exception('wut?')


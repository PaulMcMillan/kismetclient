def csv(val):
    if isinstance(val, basestring):
        return val.split(',')
    elif hasattr(val, '__iter__'):
        return ','.join(map(str, val))
    else:
        raise TypeError('Must supply a comma separated string or an iterable')

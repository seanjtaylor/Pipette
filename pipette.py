

import csv
import itertools

class Doc(dict):
    def __repr__(self):
        keys = sorted(self)
        args = ', '.join(['%s=%r' % (key, self[key]) for key in keys])
        return '%s(%s)' % (self.__class__.__name__, args)

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    __setattr__ = dict.__setitem__

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            raise AttributeError(name)


class Source(object):
    def __init__(self, source):
        self.source = source
        self.iter = self.base()

    def __iter__(self):
        return self.iter

    def base(self):
        if isinstance(self.source, str):
            with open(self.source) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    yield Doc(row)
        elif hasattr(self.source, '__iter__'):
            for item in self.source:
                yield item

    def slice(self, start_stop, stop=None):
        if stop is None:
            self.iter = itertools.islice(self.iter, start_stop)
        else:
            self.iter = itertools.islice(self.iter, start_stop, stop)
        return self

    def map(self, cbl):
        def newcbl(doc):
            return cbl(doc) or doc
        self.iter = itertools.imap(newcbl, self.iter)
        return self

    def filter(self, cbl):
        self.iter = itertools.ifilter(cbl, self.iter)
        return self

    def group_by(self, keyfunc):
        self.iter = itertools.groupby(self, keyfunc)
        return self

    def pull(self):
        self.iter = list(self)

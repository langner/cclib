from cclib.parser import ccopen


class ccCollection(object):

    def __init__(self, sources):
        self.sources = sources
        self.data = [None]*len(self.sources)

    def parse_all(self):
        for i,source in enumerate(self.sources):
            self.data[i] = ccopen(source).parse()

    def parse_next(self):
        if None in self.data:
            i = self.data.index(None)
            self.data[i] = ccopen(self.sources[i]).parse()
            return i
        else:
            return None
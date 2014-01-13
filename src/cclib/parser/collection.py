from cclib.parser import ccopen


class ccCollection(object):

    def __init__(self, sources):
        self.sources = sources
        self.data = [None]*len(self.sources)

    def parse(self):
        for i,source in enumerate(self.sources):
            self.data[i] = ccopen(source).parse()
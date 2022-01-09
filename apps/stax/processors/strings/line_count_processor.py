from apps.stax import StaxProcessor


class LineCountProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Line Count'
    FOLDER = 'strings'

    PARAMETERS = []
    INPUT_TYPES = ['string']
    OUTPUT_TYPE = 'string'

    def __init__(self):
        StaxProcessor.__init__(self)
        self.count = 1

    def process(self, params, input):
        for line in input:
            yield str(self.count)+":\t"+line
            self.count += 1

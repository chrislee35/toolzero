from apps.stax import StaxProcessor

class LineCountProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Line Count'
    FOLDER = 'data'

    PARAMETERS = []
    INPUT_TYPES = ['string']
    OUTPUT_TYPE = 'string'

    def __init__(self):
        StaxProcessor.__init__(self)
        self.count = 1

    def process(self, input):
        line = str(self.count)+":\t"+input['input']
        self.count += 1
        return line

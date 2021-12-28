from stax import StaxProcessor

class CLIInputStr(StaxProcessor):
    INITIALIZED = False
    NAME = 'CLI Input Str'
    FOLDER = 'interact'

    PARAMETERS = None
    # input is a byte buffer
    INPUT_TYPE = None
    # output is str
    OUTPUT_TYPE = 'scalar'

    def process(self, data=None):
        val = input('> ')
        self.output = val
        self.ready = self.done = True
        return val

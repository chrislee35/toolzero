from stax import StaxProcessor

class CLIPrintStr(StaxProcessor):
    INITIALIZED = False
    NAME = 'CLI Print Str'
    FOLDER = 'interact'

    PARAMETERS = None
    # input is a byte buffer
    INPUT_TYPE = 'scalar'
    # output is str
    OUTPUT_TYPE = 'scalar'

    def process(self, input=None):
        message = input['input']
        print(message)
        self.output = message
        self.ready = self.done = True
        return message

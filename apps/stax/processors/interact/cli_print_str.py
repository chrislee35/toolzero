from stax import StaxProcessor

class CLIPrintStr(StaxProcessor):
    INITIALIZED = False
    NAME = 'CLI Print Str'
    FOLDER = 'interact'

    PARAMETERS = None
    # input is a byte buffer
    INPUT_TYPE = 'string'
    # output is str
    OUTPUT_TYPE = 'string'

    def process(self, input=None):
        message = input['input']
        print(message)
        return message

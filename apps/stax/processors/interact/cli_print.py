from stax import StaxProcessor
import json

class CliPrint(StaxProcessor):
    INITIALIZED = False
    NAME = 'CLI Print'
    FOLDER = 'interact'

    PARAMETERS = None
    # input is a byte buffer
    INPUT_TYPES = ['string', 'numeric', 'dict']
    # output is str
    OUTPUT_TYPE = 'string'

    def process(self, input=None):
        message = input['input']
        if type(message) == str:
            output = message
        elif type(message) == dict:
            output = json.dumps(message, indent=2)
        else:
            output = str(message)
        print(output)
        return output

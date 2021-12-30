from stax import StaxProcessor
import json

class CliPrintList(StaxProcessor):
    INITIALIZED = False
    NAME = 'CLI Print List'
    FOLDER = 'interact'

    PARAMETERS = None
    # input is a byte buffer
    INPUT_TYPES = ['list', 'generator']
    # output is str
    OUTPUT_TYPE = 'string'

    def process(self, input=None):
        items = input['input']
        output = ""
        for message in items:
            if type(message) == str:
                output += message + '\n'
                print(message)
            elif type(message) == dict:
                output += json.dumps(message, indent=2)
                print(json.dumps(message, indent=2))
            else:
                output += str(message) + '\n'
                print(str(message))
        output = output.strip('\n')
        return output

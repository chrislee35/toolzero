from apps.stax import StaxProcessor
import json
import types


class CliPrint(StaxProcessor):
    INITIALIZED = False
    NAME = 'CLI Print'
    FOLDER = 'interact'

    PARAMETERS = []
    INPUT_TYPES = ['string', 'numeric', 'dict', 'list', 'generator']
    OUTPUT_TYPE = 'string'

    def process(self, input=None):
        message = input['input']
        if type(message) == str:
            output = message
        elif type(message) == dict:
            output = json.dumps(message, indent=2)
        elif type(message) == list or isinstance(message, types.GeneratorType):
            return self.process_list(self, message)
        else:
            output = str(message)
        print(output)
        return output

    def process_list(self, input=None):
        output = ""
        for message in input:
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

from apps.stax import StaxProcessor, StaxParameter
import json, types

class WebPrint(StaxProcessor):
    INITIALIZED = False
    NAME = 'Web Print'
    FOLDER = 'interact'

    PARAMETERS = [
        StaxParameter('output', 'textarea')
    ]
    INPUT_TYPES = ['string', 'numeric', 'dict', 'list', 'generator']
    OUTPUT_TYPE = 'string'

    def process(self, input=None):
        message = input['input']
        if type(message) == str:
            output = message
        elif type(message) == dict:
            output = json.dumps(message, indent=2)
        elif type(message) == list or type(message) == types.GeneratorType:
            return self.process_list(message);
        else:
            output = str(message)
        return output

    def process_list(self, input=None):
        output = ""
        for message in input:
            if type(message) == str:
                output += message + '\n'
            elif type(message) == dict:
                output += json.dumps(message, indent=2)
            else:
                output += str(message) + '\n'
        output = output.strip('\n')
        return output

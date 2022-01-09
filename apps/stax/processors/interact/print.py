from apps.stax import StaxProcessor, StaxParameter
import json
import types


class Print(StaxProcessor):
    INITIALIZED = False
    NAME = 'View'
    FOLDER = 'interact'

    PARAMETERS = [
        StaxParameter('output', 'textarea')
    ]
    INPUT_TYPES = ['string', 'numeric', 'dict', 'list(numeric)', 'list(string)', 'list(dict)']
    OUTPUT_TYPE = 'input'

    def process(self, params, input):
        for message in input:
            if type(message) == str:
                output = message
            elif type(message) == dict:
                output = json.dumps(message, indent=2)
            elif type(message) == list or isinstance(message, types.GeneratorType):
                output = self.process_list(message)
            else:
                output = str(message)
            self.send_output(params['id'], output)
            yield message

    def process_list(self, input):
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

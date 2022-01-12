from apps.stax import StaxProcessor


class MakeListProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Make List'
    FOLDER = 'datastructures'

    PARAMETERS = []
    INPUT_TYPES = ['numeric', 'string', 'dict']
    OUTPUT_TYPE = 'rule'
    OUTPUT_TYPES = ['list(numeric)', 'list(string)', 'list(dict)']

    def process(self, params, input):
        yield list(input)

    def determine_output(self, input_type):
        if input_type == 'numeric':
            return 'list(numeric)'
        elif input_type == 'string':
            return 'list(string)'
        elif input_type == 'dict':
            return 'list(dict)'

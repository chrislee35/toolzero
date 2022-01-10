from apps.stax import StaxProcessor, StaxParameter, ComboboxParameter
import types


class ExtractProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Extract Elements'
    FOLDER = 'datastructures'

    PARAMETERS = [
        StaxParameter('field', 'string', 'name')
    ]
    INPUT_TYPES = ['list(numeric)', 'list(string)', 'dict']
    OUTPUT_TYPE = 'rule'
    OUTPUT_TYPES = ['numeric', 'string', 'dict']

    def process(self, params, input):
        field = params['field']
        for item in input:
            if type(item) == dict:
                yield item.get(field)
            elif type(item) == list:
                yield item[int(field)]
            else:
                yield None

    def determine_output(self, input_type):
        if input_type == 'list(numeric)':
            return 'numeric'
        elif input_type == 'list(string)':
            return 'string'
        elif input_type == 'dict':
            return 'select'

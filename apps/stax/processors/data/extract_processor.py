from apps.stax import StaxProcessor, StaxParameter
import types


class ExtractProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Extract Elements'
    FOLDER = 'data'

    PARAMETERS = [
        StaxParameter('field', 'string', 'name')
    ]
    INPUT_TYPES = ['list', 'generator', 'dict']
    OUTPUT_TYPE = 'generator'

    def process(self, input):
        field = input['params']['field']
        if type(input['input']) == list or isinstance(input['input'], types.GeneratorType):
            for item in input['input']:
                if type(item) == dict:
                    yield item.get(field)
                elif type(item) == list:
                    yield item[int(field)]
                else:
                    yield None
        else:
            yield item.get(field)

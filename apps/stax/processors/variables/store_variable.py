from apps.stax import StaxProcessor, StaxParameter
import inspect


class StoreVariable(StaxProcessor):
    INITIALIZED = False
    NAME = 'Store Variable'
    FOLDER = 'data'

    PARAMETERS = [
        StaxParameter('name', 'string', 'x')
    ]
    INPUT_TYPES = ['list', 'string', 'numeric', 'dict', 'generator',
        'bytes_generator']
    OUTPUT_TYPE = 'None'

    def process(self, input):
        value = input['input']
        name = input['params']['name']

        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        calframe[1].frame.f_locals['self'].set_variable(name, value)
        return None

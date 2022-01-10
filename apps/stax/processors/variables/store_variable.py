from apps.stax import StaxProcessor, StaxParameter, StaxStore
import inspect


class StoreVariable(StaxProcessor):
    INITIALIZED = False
    NAME = 'Store Variable'
    FOLDER = 'variables'

    PARAMETERS = [
        StaxParameter('name', 'string', 'x')
    ]
    INPUT_TYPES = ['list(string)', 'list(numeric)', 'list(dict)', 'string', 'numeric', 'dict', 'bytes']
    OUTPUT_TYPE = 'None'

    def process(self, params, input):
        name = params['name']
        StaxStore.set(name, input)
        return None

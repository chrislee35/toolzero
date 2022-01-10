from apps.stax import StaxProcessor, StaxParameter, ComboboxParameter, StaxStore
import inspect


class LoadVariable(StaxProcessor):
    INITIALIZED = False
    NAME = 'Load Variable'
    FOLDER = 'variables'

    PARAMETERS = [
        StaxParameter('Variable', 'string', 'x')
    ]
    INPUT_TYPES = ['None']
    OUTPUT_TYPE = 'select'
    OUTPUT_TYPES = ['string', 'numeric', 'dict', 'list(string)', 'list(numeric)', 'bytes']

    def process(self, params, input):
        name = params['Variable']
        val = StaxStore.get(name)
        if val is None:
            yield None
        else:
            return val

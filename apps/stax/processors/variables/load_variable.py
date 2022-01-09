from apps.stax import StaxProcessor, StaxParameter, ComboboxParameter
import inspect


class LoadVariable(StaxProcessor):
    INITIALIZED = False
    NAME = 'Load Variable'
    FOLDER = 'variables'

    PARAMETERS = [
        ComboboxParameter('Variable Type', ['string', 'numeric', 'dict', 'list(string)', 'list(numeric)', 'bytes']),
        StaxParameter('Variable', 'string', 'x')
    ]
    INPUT_TYPES = ['None']
    OUTPUT_TYPE = 'select'

    def process(self, params, input):
        variable = params['Variable']
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        return calframe[1].frame.f_locals['self'].variables[variable]

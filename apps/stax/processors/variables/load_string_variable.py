from apps.stax import StaxProcessor, StaxParameter
import inspect


class LoadStringVariable(StaxProcessor):
    INITIALIZED = False
    NAME = 'Load String Variable'
    FOLDER = 'data'

    PARAMETERS = [
        StaxParameter('Variable', 'string', 'x')
    ]
    INPUT_TYPES = ['None']
    OUTPUT_TYPE = 'string'

    def process(self, input):
        variable = input['params']['Variable']
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        return calframe[1].frame.f_locals['self'].variables[variable]

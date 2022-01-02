from apps.stax import StaxProcessor, StaxParameter
import inspect

class LoadNumericVariable(StaxProcessor):
    INITIALIZED = False
    NAME = 'Load Numeric Variable'
    FOLDER = 'data'

    PARAMETERS = [
        StaxParameter('Variable', 'string', 'x')
    ]
    INPUT_TYPES = ['None']
    OUTPUT_TYPE = 'numeric'

    def process(self, input):
        variable = input['params']['Variable']
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        return calframe[1].frame.f_locals['self'].variables[variable]

from apps.stax import StaxProcessor, StaxParameter
import inspect

class LoadBytesGeneratorVariable(StaxProcessor):
    INITIALIZED = False
    NAME = 'Load Bytes Generator Variable'
    FOLDER = 'data'

    PARAMETERS = [
        StaxParameter('Variable', 'string', 'x')
    ]
    INPUT_TYPES = ['None']
    OUTPUT_TYPE = 'bytes_generator'

    def process(self, input):
        variable = input['params']['Variable']
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        return calframe[1].frame.f_locals['self'].variables[variable]

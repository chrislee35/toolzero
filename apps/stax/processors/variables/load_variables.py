from apps.stax import StaxProcessor
import inspect


class LoadVariables(StaxProcessor):
    INITIALIZED = False
    NAME = 'Load All Variables'
    FOLDER = 'variables'

    PARAMETERS = []
    INPUT_TYPES = ['None']
    OUTPUT_TYPE = 'dict'

    def process(self, params, input):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        return calframe[1].frame.f_locals['self'].variables

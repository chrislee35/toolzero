from apps.stax import StaxProcessor
import inspect


class LoadVariables(StaxProcessor):
    INITIALIZED = False
    NAME = 'Load All Variables'
    FOLDER = 'data'

    PARAMETERS = []
    INPUT_TYPES = ['None']
    OUTPUT_TYPE = 'dict'

    def process(self, input):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        return calframe[1].frame.f_locals['self'].variables

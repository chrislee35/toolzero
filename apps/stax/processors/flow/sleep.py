from apps.stax import StaxProcessor, StaxParameter
import time

class Sleep(StaxProcessor):
    INITIALIZED = False
    NAME = 'Sleep'
    FOLDER = 'flow'

    PARAMETERS = [
        StaxParameter('seconds', 'numeric', 10)
    ]
    INPUT_TYPES = ['None', 'string', 'numeric', 'dict', 'list(string)', 'list(numeric)', 'list(dict)', 'bytes']
    OUTPUT_TYPE = 'input'

    def process(self, params, input=None):
        for item in input:
            time.sleep(params['seconds'])
            yield item

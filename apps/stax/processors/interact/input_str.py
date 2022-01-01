from apps.stax import StaxProcessor, StaxParameter

class InputStr(StaxProcessor):
    INITIALIZED = False
    NAME = 'Input String'
    FOLDER = 'interact'

    PARAMETERS = [
        StaxParameter('string', 'string', 'test')
    ]
    INPUT_TYPES = ['None']
    OUTPUT_TYPE = 'string'

    def process(self, input=None):
        val = input['params']['string']
        return val

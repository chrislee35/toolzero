from stax import StaxProcessor, StaxParameter

class InputStr(StaxProcessor):
    INITIALIZED = False
    NAME = 'Input String'
    FOLDER = 'interact'

    PARAMETERS = [
        StaxParameter('String', 'string', 'test')
    ]
    INPUT_TYPE = None
    OUTPUT_TYPE = 'string'

    def process(self, input=None):
        val = input['params']['String']
        return val

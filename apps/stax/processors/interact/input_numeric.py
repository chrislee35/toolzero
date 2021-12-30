from stax import StaxProcessor, StaxParameter

class InputNumeric(StaxProcessor):
    INITIALIZED = False
    NAME = 'Input Number'
    FOLDER = 'interact'

    PARAMETERS = [
        StaxParameter('Number', 'float', '4.3')
    ]
    INPUT_TYPE = None
    OUTPUT_TYPE = 'numeric'

    def process(self, input=None):
        val = input['params']['Number']
        return float(val)

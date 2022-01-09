from apps.stax import StaxProcessor, StaxParameter


class InputNumeric(StaxProcessor):
    INITIALIZED = False
    NAME = 'Input Number'
    FOLDER = 'interact'

    PARAMETERS = [
        StaxParameter('number', 'float', '4.3')
    ]
    INPUT_TYPES = ['None']
    OUTPUT_TYPE = 'numeric'

    def process(self, params, input):
        val = params['number']
        yield float(val)

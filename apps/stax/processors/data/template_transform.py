from stax import StaxProcessor, StaxParameter

class TemplateTransform(StaxProcessor):
    INITIALIZED = False
    NAME = 'Template Transform'
    FOLDER = 'data'

    PARAMETERS = [
        StaxParameter('template', 'string', '{}')
    ]
    # input is a byte buffer
    INPUT_TYPES = ['string', 'numeric']
    # output is str
    OUTPUT_TYPE = 'string'

    def process(self, input=None):
        template = input['params']['template']
        if template:
            val = template.format(input['input'])
        else:
            val = input['input']
        return val

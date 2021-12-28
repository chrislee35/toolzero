from stax import StaxProcessor, StaxParameter

class TemplateTransform(StaxProcessor):
    INITIALIZED = False
    NAME = 'Template Transform'
    FOLDER = 'data'

    PARAMETERS = [
        StaxParameter('template', 'string')
    ]
    # input is a byte buffer
    INPUT_TYPE = 'scalar'
    # output is str
    OUTPUT_TYPE = 'scalar'

    def process(self, input=None):
        template = input['params']['template']
        if template:
            val = template.format(input['input'])
        else:
            val = input['input']

        self.output = val
        self.ready = self.done = True
        return val

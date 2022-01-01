from apps.stax import StaxProcessor, StaxParameter

class TemplateTransform(StaxProcessor):
    INITIALIZED = False
    NAME = 'Template Transform'
    FOLDER = 'data'

    PARAMETERS = [
        StaxParameter('template', 'string', '{x} is different than {y}')
    ]
    # input is a byte buffer
    INPUT_TYPES = ['string', 'numeric', 'dict', 'list']
    # output is str
    OUTPUT_TYPE = 'string'

    def process(self, input=None):
        template = input['params']['template']
        print(input['input'])
        if not template:
            val = input['input']
        elif type(input['input']) == dict:
            val = template.format(**input['input'])
        elif type(input['input']) == list:
            val = template.format(*input['input'])
        else:
            val = input['input'].format(input['input'])
        return val

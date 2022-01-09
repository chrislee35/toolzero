from apps.stax import StaxProcessor, StaxParameter


class TemplateTransform(StaxProcessor):
    INITIALIZED = False
    NAME = 'Template Transform'
    FOLDER = 'strings'

    PARAMETERS = [
        StaxParameter('template', 'string', '{x} is different than {y}')
    ]
    INPUT_TYPES = ['string', 'numeric', 'dict', 'list(string)', 'list(numeric)']
    OUTPUT_TYPE = 'string'

    def process(self, input=None):
        template = params['template']
        if not template:
            val = input
        elif type(input) == dict:
            val = template.format(**input)
        elif type(input) == list:
            val = template.format(*input)
        else:
            val = template.format(input)
        return val

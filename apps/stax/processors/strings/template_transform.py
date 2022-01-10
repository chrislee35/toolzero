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

    def process(self, params, input):
        template = params['template']
        for item in input:
            if not template:
                val = item
            elif type(item) == dict:
                val = template.format(**item)
            elif type(item) == list:
                val = template.format(*item)
            else:
                val = template.format(item)
            yield val

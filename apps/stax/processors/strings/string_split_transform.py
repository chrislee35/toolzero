from apps.stax import StaxProcessor, StaxParameter


class StringSplitTransform(StaxProcessor):
    INITIALIZED = False
    NAME = 'String Split'
    FOLDER = 'strings'

    PARAMETERS = [
        StaxParameter('delimeter', 'string', '\\n')
    ]
    INPUT_TYPES = ['string']
    OUTPUT_TYPE = 'list(string)'

    def process(self, params, input):
        string = input
        delim = params['delimeter'].replace('\\n', '\n').replace('\\t', '\t')
        for s in string:
            yield s.split(delim)

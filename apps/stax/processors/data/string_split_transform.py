from apps.stax import StaxProcessor, StaxParameter


class StringSplitTransform(StaxProcessor):
    INITIALIZED = False
    NAME = 'String Split'
    FOLDER = 'data'

    PARAMETERS = [
        StaxParameter('delimeter', 'string', '\\n')
    ]
    INPUT_TYPES = ['string', 'generator']
    OUTPUT_TYPE = 'list'

    def process(self, input):
        string = input['input']
        delim = input['params']['delimeter'].replace('\\n', '\n').replace('\\t', '\t')
        if type(string) == str:
            return string.split(delim)
        else:
            for s in string:
                yield s.split(delim)

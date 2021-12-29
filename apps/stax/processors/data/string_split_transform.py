from stax import StaxProcessor, StaxParameter

class StringSplitTransform(StaxProcessor):
    INITIALIZED = False
    NAME = 'String Split'
    FOLDER = 'data'

    PARAMETERS = [
        StaxParameter('delimeter', 'string', '\n')
    ]
    INPUT_TYPE = 'string'
    OUTPUT_TYPE = 'list'

    def process(self, input):
        string = input['input']
        delim = input['params']['delimeter']
        return string.split(delim)

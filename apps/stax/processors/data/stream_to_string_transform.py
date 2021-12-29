from stax import StaxProcessor, StaxParameter

class StreamToStringTransform(StaxProcessor):
    INITIALIZED = False
    NAME = 'Stream to String'
    FOLDER = 'data'

    PARAMETERS = None
    INPUT_TYPE = 'stream'
    OUTPUT_TYPE = 'string'

    def process(self, input):
        buf = ""
        for item in input['input']:
            buf += str(item.decode('UTF-8'))
        return buf

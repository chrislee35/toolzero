from apps.stax import StaxProcessor, StaxParameter

class StreamToStringTransform(StaxProcessor):
    INITIALIZED = False
    NAME = 'Stream to String'
    FOLDER = 'data'

    PARAMETERS = []
    INPUT_TYPES = ['bytes_generator']
    OUTPUT_TYPE = 'string'

    def process(self, input):
        buf = ""
        for item in input['input']:
            buf += str(item.decode('UTF-8'))
        return buf

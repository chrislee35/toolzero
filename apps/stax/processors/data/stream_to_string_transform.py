from apps.stax import StaxProcessor, StaxParameter


class StreamToStringTransform(StaxProcessor):
    INITIALIZED = False
    NAME = 'Stream to String'
    FOLDER = 'data'

    PARAMETERS = [
        StaxParameter('encoding', 'string', 'UTF-8')
    ]
    INPUT_TYPES = ['bytes_generator']
    OUTPUT_TYPE = 'generator'

    def process(self, input):
        encoding = input['params']['encoding']
        for item in input['input']:
            yield str(item.decode(encoding))

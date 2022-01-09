from apps.stax import StaxProcessor, StaxParameter


class StreamToStringTransform(StaxProcessor):
    INITIALIZED = False
    NAME = 'Stream to String'
    FOLDER = 'bytes'

    PARAMETERS = [
        StaxParameter('encoding', 'string', 'UTF-8')
    ]
    INPUT_TYPES = ['bytes']
    OUTPUT_TYPE = 'string'

    def process(self, params, input):
        encoding = params['encoding']
        for item in input:
            yield str(item.decode(encoding))

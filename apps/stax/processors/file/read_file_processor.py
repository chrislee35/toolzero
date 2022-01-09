from apps.stax import StaxProcessor


class ReadFileProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Read File'
    FOLDER = 'file'

    PARAMETERS = []
    INPUT_TYPES = ['string']
    OUTPUT_TYPE = 'bytes'

    def process(self, params, input):
        for filename in input:
            with open(filename, 'rb') as fh:
                buff = fh.read(1024)
                while buff:
                    yield buff
                    buff = fh.read(1024)
                yield None

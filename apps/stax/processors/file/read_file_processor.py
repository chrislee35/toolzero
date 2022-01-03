from apps.stax import StaxProcessor


class ReadFileProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Read File'
    FOLDER = 'file'

    PARAMETERS = []
    INPUT_TYPES = ['string']
    OUTPUT_TYPE = 'bytes_generator'

    def process(self, input):
        filename = input['input']
        with open(filename, 'rb') as fh:
            buff = fh.read(1024)
            while buff:
                yield buff
                buff = fh.read(1024)

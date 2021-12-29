import tempfile
from stax import StaxProcessor

class ReadFileProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Read File'
    FOLDER = 'file'

    PARAMETERS = None
    # input is a byte buffer
    INPUT_TYPE = 'string'
    # output is filename
    OUTPUT_TYPE = 'stream'

    def process(self, input):
        filename = input['input']
        with open(filename, 'rb') as fh:
            buff = fh.read(1024)
            yield buff

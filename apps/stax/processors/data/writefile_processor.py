import tempfile
from stax import StaxProcessor

class WriteFileProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Write File'
    FOLDER = 'file'

    PARAMETERS = None
    # input is a byte buffer
    INPUT_TYPE = 'stream'
    # output is filename
    OUTPUT_TYPE = 'string'

    def process(self, input):
        generator = input['input']
        tmpfile = tempfile.NamedTemporaryFile(delete=False)
        for buffer in generator:
            tmpfile.write(buffer)
            tmpfile.close()
        return tmpfile.name

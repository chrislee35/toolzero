import tempfile
from stax import StaxProcessor

class WriteFileProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Write File'
    FOLDER = 'file'

    PARAMETERS = None
    # input is a byte buffer
    INPUT_TYPE = 'raw'
    # output is filename
    OUTPUT_TYPE = 'scalar'

    def __init__(self):
        self.tmpfile = tempfile.NamedTemporaryFile()

    def process(self, input):
        self.output = False
        self.ready = self.done = False
        buffer = input['buffer']
        self.tmpfile.write(buffer)

    def end_record(self):
        filename = self.tmpfile.name
        self.tmpfile = tempfile.NamedTemporaryFile()
        self.ready = self.done = True
        self.output = filename
        return filename

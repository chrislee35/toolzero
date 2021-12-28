import tempfile
from stax import StaxProcessor, StaxParameter

class MoveFileProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Move File'
    FOLDER = 'file'

    PARAMETERS = [
        StaxParameter('destination', 'string')
    ]
    # input is a byte buffer
    INPUT_TYPE = 'filename'
    # output is filename
    OUTPUT_TYPE = 'filename'

    def process(self, input):
        src_filename = input['input']
        dst_filename = input['params']['destination']
        os.rename(src_filename, dst_filename)
        self.output = dst_filename
        self.ready = self.done = True
        return dst_filename

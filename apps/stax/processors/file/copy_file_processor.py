import shutil
from stax import StaxProcessor, StaxParameter

class CopyFileProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Copy File'
    FOLDER = 'file'

    PARAMETERS = [
        StaxParameter('destination', 'string', 'test2')
    ]
    # input is a byte buffer
    INPUT_TYPES = ['string']
    # output is filename
    OUTPUT_TYPE = 'string'

    def process(self, input):
        src_filename = input['input']
        dst_filename = input['params']['destination']
        shutil.copy(src_filename, dst_filename)
        return dst_filename

import os
from stax import StaxProcessor, StaxParameter

class MoveFileProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Move File'
    FOLDER = 'file'

    PARAMETERS = [
        StaxParameter('destination', 'string')
    ]
    # input is a byte buffer
    INPUT_TYPES = ['string']
    # output is filename
    OUTPUT_TYPE = 'string'

    def process(self, input):
        src_filename = input['input']
        dst_filename = input['params']['destination']
        os.rename(src_filename, dst_filename)
        return dst_filename

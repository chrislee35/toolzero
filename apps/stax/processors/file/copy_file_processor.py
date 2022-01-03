import shutil
from apps.stax import StaxProcessor, StaxParameter


class CopyFileProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Copy File'
    FOLDER = 'file'

    PARAMETERS = [
        StaxParameter('destination', 'string', 'test2')
    ]
    INPUT_TYPES = ['string']
    OUTPUT_TYPE = 'string'

    def process(self, input):
        src_filename = input['input']
        dst_filename = input['params']['destination']
        shutil.copy(src_filename, dst_filename)
        return dst_filename

import tempfile
from stax import StaxProcessor, StaxParameter

class XorStreamProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'XOR'
    FOLDER = 'data'

    PARAMETERS = [
        StaxParameter('xor', 'string', '0xa5')
    ]
    # input is a byte buffer
    INPUT_TYPES = ['bytes_generator']
    # output is filename
    OUTPUT_TYPE = 'bytes_generator'

    def process(self, input):
        generator = input['input']
        for buffer in generator:
            xor = bytes.fromhex(input['params']['xor'].replace('0x',''))
            xor_buffer = bytes([xor[0]^c for c in buffer])
            yield xor_buffer

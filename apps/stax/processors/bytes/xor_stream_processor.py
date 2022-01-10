from apps.stax import StaxProcessor, StaxParameter


class XorStreamProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'XOR'
    FOLDER = 'bytes'

    PARAMETERS = [
        StaxParameter('xor', 'string', '0xa5')
    ]
    # input is a byte buffer
    INPUT_TYPES = ['bytes']
    # output is filename
    OUTPUT_TYPE = 'bytes'

    def process(self, params, input):
        generator = input
        for buffer in generator:
            if buffer is None:
                continue
            xor = bytes.fromhex(params['xor'].replace('0x', ''))
            xor_buffer = bytes([xor[0] ^ c for c in buffer])
            yield xor_buffer

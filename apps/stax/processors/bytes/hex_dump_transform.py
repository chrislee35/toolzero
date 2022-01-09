from apps.stax import StaxProcessor


class HexDumpTransform(StaxProcessor):
    INITIALIZED = False
    NAME = 'Hex Dump'
    FOLDER = 'bytes'

    PARAMETERS = []
    INPUT_TYPES = ['bytes']
    OUTPUT_TYPE = 'string'

    def process(self, input=None):
        buffer = b''
        offset = 0
        for buf in input:
            buffer += buf
            while len(buffer) >= 16:
                line = "%04x: %s  %s" % (offset,
                    buffer[0:16].hex(sep=' '),
                    self.buf_2_ascii(buffer[0:16])
                )
                buffer = buffer[16:]
                offset += 16
                yield line

        if len(buffer) > 0:
            line = "%04x: %s  %s" % (offset,
                buffer[0:16].hex(sep=' ').ljust(47),
                self.buf_2_ascii(buffer)
            )
            yield line

    def buf_2_ascii(self, buf):
        ascii = ''
        for byte in buf:
            if 0x20 <= byte <= 0x7E:
                ascii += chr(byte)
            else:
                ascii += '.'
        return ascii

import tempfile
import json
from apps.stax import StaxProcessor, StaxParameter


class WriteFileProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Write File'
    FOLDER = 'file'

    PARAMETERS = [
        StaxParameter('list join charater', 'string', ', '),
        StaxParameter('add newline', 'string', 'no'),
        StaxParameter('encoding', 'string', 'UTF-8')
    ]
    # input is a byte buffer
    INPUT_TYPES = ['bytes_generator', 'generator']
    # output is filename
    OUTPUT_TYPE = 'string'

    def process(self, input):
        generator = input['input']
        tmpfile = tempfile.NamedTemporaryFile(delete=False)
        for buffer in generator:
            if type(buffer) == dict:
                json.dump(buffer, tmpfile, indent=2)
            elif type(buffer) in [str, bytes]:
                tmpfile.write(buffer.encode(input['params']['encoding']))
            elif type(buffer) == list:
                tmpfile.write(
                    input['params']['list join character'].join(
                        [str(x) for x in buffer]
                    )
                )
            if input['params']['add newline'] != 'no':
                tmpfile.write('\n'.encode(input['params']['encoding']))
        tmpfile.close()
        return tmpfile.name

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
    INPUT_TYPES = ['bytes', 'string', 'dict', 'list(string)', 'list(numeric)']
    OUTPUT_TYPE = 'string'

    def process(self, params, input):
        tmpfile = tempfile.NamedTemporaryFile(delete=False)
        for buffer in input:
            if buffer is None:
                tmpfile.close()
                yield tmpfile.name
                tmpfile = tempfile.NamedTemporaryFile(delete=False)
            else:
                if type(buffer) == dict:
                    json.dump(buffer, tmpfile, indent=2)
                elif type(buffer) == str:
                    tmpfile.write(buffer.encode(params['encoding']))
                elif type(buffer) == bytes:
                    tmpfile.write(buffer)
                elif type(buffer) == list:
                    tmpfile.write(
                        params['list join character'].join(
                            [str(x) for x in buffer]
                        )
                    )
                if params['add newline'] != 'no':
                    tmpfile.write('\n'.encode(params['encoding']))

        tmpfile.close()
        yield tmpfile.name

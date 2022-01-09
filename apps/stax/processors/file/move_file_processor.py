import os
from apps.stax import StaxProcessor, StaxParameter


class MoveFileProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Move File'
    FOLDER = 'file'

    PARAMETERS = [
        StaxParameter('destination', 'string')
    ]
    PARAMETERS = [
        StaxParameter('overwrite?', 'boolean', False),
        StaxParameter('count up?', 'boolean', True),
        StaxParameter('destination', 'string', 'test')
    ]
    INPUT_TYPES = ['string']
    OUTPUT_TYPE = 'string'

    def process(self, params, input):
        overwrite = params['overwrite?']
        count_up = params['count_up']
        write = True
        for src_filename in input:
            dst_filename = params['destination']
            if not overwrite and os.path.exists(dst_filename):
                if count_up:
                    counter = 1
                    while os.path.exists(dst_filename+str(counter)):
                        counter += 1
                    dst_filename+str(counter)
                else:
                    write = False
                    self.send_output('Move File will not overwrite '+dst_filename)
            if write:
                os.rename(src_filename, dst_filename)
                yield dst_filename

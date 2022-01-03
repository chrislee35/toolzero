from apps.stax import StaxProcessor, StaxParameter, ComboboxParameter
import re


class GrepProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Grep'
    FOLDER = 'data'

    PARAMETERS = [
        StaxParameter('filter', 'string', 'test.ng'),
        ComboboxParameter('grep type', ['fixed', 'regex'], 'regex'),
        StaxParameter('inverse', 'boolean', False),
        StaxParameter('only matching', 'boolean', False),
        StaxParameter('unicode match', 'boolean', True),
        StaxParameter('multiline match', 'boolean', False),
        StaxParameter('case insensitive match', 'boolean', True),
        StaxParameter('dotall match', 'boolean', False)
    ]
    INPUT_TYPES = ['list', 'generator']
    OUTPUT_TYPE = 'generator'

    def process(self, input):
        filter = input['params']['filter']
        grep_type = input['params']['grep type']
        inverse = input['params']['inverse']
        only_matching = input['params']['only matching']

        if grep_type == 'regex':
            rexp = re.compile(input['params']['filter'])
            flags = 0
            if input['params']['unicode match']:
                flags += re.U
            if input['params']['multiline match']:
                flags += re.M
            if input['params']['case insensitive match']:
                flags += re.I
            if input['params']['dotall']:
                flags += re.DOTALL

        for line in input['input']:
            if grep_type == 'regex':
                m = rexp.search(line)
                if not m and inverse:
                    yield line
                elif m and only_matching:
                    yield m.group(0)
                elif m:
                    yield line
            else:
                if filter in line and not inverse:
                    yield line
                elif filter not in line and inverse:
                    yield line

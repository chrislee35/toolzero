from apps.stax import StaxProcessor, StaxParameter, ComboboxParameter
import re


class GrepProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Grep'
    FOLDER = 'strings'

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
    INPUT_TYPES = ['string']
    OUTPUT_TYPE = 'string'

    def process(self, params, input):
        filter = params['filter']
        grep_type = params['grep type']
        inverse = params['inverse']
        only_matching = params['only matching']

        if grep_type == 'regex':
            rexp = re.compile(params['filter'])
            flags = 0
            if params['unicode match']:
                flags += re.U
            if params['multiline match']:
                flags += re.M
            if params['case insensitive match']:
                flags += re.I
            if params['dotall']:
                flags += re.DOTALL

        for line in input:
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

import requests
from stax import StaxProcessor

class RestProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'REST'
    # which folder of processors should this processor appear
    # None means that it doesn't appear anywhere
    FOLDER = 'web' # should be str

    # list of StaxParameter objects with the parameters to the processor
    PARAMETERS = None
    # input is a single URL
    INPUT_TYPE = 'scalar'
    # output is the decoded json
    OUTPUT_TYPE = 'dict'

    def process(self, input):
        self.output = None
        url = input['input']
        if url:
            r = requests.get(url)
            self.output = r.json()
        self.ready = self.done = True

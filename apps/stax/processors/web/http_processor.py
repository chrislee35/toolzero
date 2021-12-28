import requests
from stax import StaxProcessor

class HttpProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'HTTP'
    # which folder of processors should this processor appear
    # None means that it doesn't appear anywhere
    FOLDER = 'web' # should be str

    # list of StaxParameter objects with the parameters to the processor
    PARAMETERS = None
    # input is a single URL
    INPUT_TYPE = 'scalar'
    # output is the byte buffer
    OUTPUT_TYPE = 'raw'

    def process(self, input):
        self.output = None
        self.ready = self.done = False
        url = input['input']
        if url:
            r = requests.get(url)
            self.output = r.iter_content(chunk_size=1024)
        else:
            self.ready = self.done = True
            return None

    def continue(self):
        next(self.output)

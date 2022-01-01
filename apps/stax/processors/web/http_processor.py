import requests
from apps.stax import StaxProcessor

class HttpProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'HTTP'
    # which folder of processors should this processor appear
    # None means that it doesn't appear anywhere
    FOLDER = 'web' # should be str

    # list of StaxParameter objects with the parameters to the processor
    PARAMETERS = []
    # input is a single URL
    INPUT_TYPES = ['string']
    # output is the byte buffer
    OUTPUT_TYPE = 'stream'

    def process(self, input):
        url = input['input']
        if url:
            r = requests.get(url)
            for chunk in r.iter_content(chunk_size=1024):
                return chunk
        else:
            yield None

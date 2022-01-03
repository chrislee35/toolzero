import requests
from apps.stax import StaxProcessor


class HttpProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'HTTP'
    FOLDER = 'web'

    PARAMETERS = []
    INPUT_TYPES = ['string']
    OUTPUT_TYPE = 'stream'

    def process(self, input):
        url = input['input']
        if url:
            r = requests.get(url)
            for chunk in r.iter_content(chunk_size=1024):
                return chunk
        else:
            yield None

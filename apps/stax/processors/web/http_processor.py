import requests
from apps.stax import StaxProcessor


class HttpProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'HTTP Get'
    FOLDER = 'web'

    PARAMETERS = []
    INPUT_TYPES = ['string']
    OUTPUT_TYPE = 'bytes'

    def process(self, params, input):
        for url in input:
            r = requests.get(url)
            for chunk in r.iter_content(chunk_size=1024):
                yield chunk
            yield None

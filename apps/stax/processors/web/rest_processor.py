import requests
from apps.stax import StaxProcessor


class RestProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'REST Get'
    FOLDER = 'web'

    PARAMETERS = []
    INPUT_TYPES = ['string']
    OUTPUT_TYPE = 'dict'

    def process(self, params, input):
        for url in input:
            r = requests.get(url)
            yield r.json()

import requests
from apps.stax import StaxProcessor


class RestProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'REST'
    FOLDER = 'web'

    PARAMETERS = []
    INPUT_TYPES = ['string']
    OUTPUT_TYPE = 'dict'

    def process(self, input):
        self.output = None
        url = input['input']
        if url:
            r = requests.get(url)
            self.output = r.json()
        self.ready = self.done = True

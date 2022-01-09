from apps.stax import StaxProcessor


class Null(StaxProcessor):
    INITIALIZED = False
    NAME = 'Null'
    FOLDER = 'flow'

    PARAMETERS = []
    INPUT_TYPES = ['string', 'numeric', 'dict', 'bytes']
    OUTPUT_TYPE = 'None'

    def process(self, params, input):
        return None

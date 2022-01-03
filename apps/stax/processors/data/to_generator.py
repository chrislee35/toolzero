from apps.stax import StaxProcessor


class ToGenerator(StaxProcessor):
    INITIALIZED = False
    NAME = 'To Generator'
    FOLDER = 'data'

    PARAMETERS = []
    INPUT_TYPES = ['string', 'numeric', 'dict', 'list']
    OUTPUT_TYPE = 'generator'

    def process(self, input=None):
        item = input['input']
        if type(item) == list:
            return item
        else:
            yield item

from apps.stax import StaxProcessor, StaxParameter


class SelectListItem(StaxProcessor):
    INITIALIZED = False
    NAME = 'Select List Item'
    FOLDER = 'data'

    PARAMETERS = [
        StaxParameter('index', 'number', 0)
    ]
    INPUT_TYPES = ['list', 'generator']
    OUTPUT_TYPE = 'string'

    def process(self, input):
        index = input['params']['index']
        for i, v in enumerate(input['input']):
            if i == index:
                return v

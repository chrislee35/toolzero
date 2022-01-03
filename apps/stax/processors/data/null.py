from apps.stax import StaxProcessor


class Null(StaxProcessor):
    INITIALIZED = False
    NAME = 'Null'
    FOLDER = 'data'

    PARAMETERS = []
    INPUT_TYPES = ['list', 'string', 'numeric', 'dict', 'generator',
        'bytes_generator']
    OUTPUT_TYPE = 'None'

    def process(self, input):
        return None

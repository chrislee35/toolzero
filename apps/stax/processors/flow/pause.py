from apps.stax import StaxProcessor


class Pause(StaxProcessor):
    INITIALIZED = False
    NAME = 'Pause'
    FOLDER = 'flow'

    PARAMETERS = []
    INPUT_TYPES = ['None', 'string', 'numeric', 'dict', 'list(string)', 'list(numeric)', 'list(dict)', 'bytes']
    OUTPUT_TYPE = 'input'

    def process(self, params, input=None):
        self.pause()
        return input

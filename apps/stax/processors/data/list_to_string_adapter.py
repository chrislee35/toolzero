from apps.stax import StaxProcessor


class ListToStringAdapter(StaxProcessor):
    INITIALIZED = False
    NAME = 'List to String'
    FOLDER = 'data'

    PARAMETERS = []
    INPUT_TYPES = ['list', 'generator']
    OUTPUT_TYPE = 'string'

    def process(self, input):
        mylist = input['input']
        for item in mylist:
            yield item

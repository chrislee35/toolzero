from stax import StaxProcessor, StaxParameter

class ListToStringAdapter(StaxProcessor):
    INITIALIZED = False
    NAME = 'List to String'
    FOLDER = 'data'

    PARAMETERS = None
    INPUT_TYPE = 'list'
    OUTPUT_TYPE = 'string'

    def process(self, input):
        mylist = input['input']
        for item in mylist:
          yield item

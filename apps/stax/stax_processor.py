class StaxProcessor:
    INITIALIZED = False
    NAME = 'StaxProcessor'
    # which folder of processors should this processor appear
    # None means that it doesn't appear anywhere
    FOLDER = 'None'  # should be str
    # description of the tool
    DESCRIPTION = "Base class for all Stax Processors"

    # list of StaxParameter or ComboboxParameter objects with the parameters to the processor
    PARAMETERS = []
    # valid types:
    # 'None', 'string', 'numeric', 'dict', 'bytes'
    # 'list(string)', 'list(numeric)', 'list(dict)'
    INPUT_TYPES = ['None']
    OUTPUT_TYPE = 'None'

    def __init__(self, parent):
        self.parent = parent
        self.input_type = 'None'
        self.output_type = 'None'

    def pause(self):
        self.parent.pause()

    def send_output(self, id, message):
        self.parent.send_output(id, message)

    def get_valid_input_types(self):
        return self.INPUT_TYPES

    def get_output_type(self):
        return self.output_type

    def set_input_type(self, input_type):
        valid = input_type in self.get_valid_input_types()
        if not valid:
            raise Exception("%s cannot accept type %s" % (self.__class__.__name__, input_type))
        self.input_type = input_type
        self.output_type = self.OUTPUT_TYPE
        if self.output_type == 'input':
            self.output_type = self.input_type
        elif self.output_type == 'rule':
            self.output_type = self.determine_output(self.input_type)

        return self.output_type

    def determine_output(self, input_type):
        return 'unknown'

    @classmethod
    def create(cls, **kwargs):
        if not cls.INITIALIZED:
            cls.intialize()

        # return an instance of this class
        return cls(**kwargs)

    @classmethod
    def intialize(cls):
        # generate any resources that are shared across all instances of this type of processor
        # on success, it must set the INITIALIZED flag for the class to True
        cls.INITIALIZED = True

    @classmethod
    def get_parameters(cls):
        """ returns a list of StaxParameter objects with the parameters to the processor """
        return cls.PARAMETERS

    def process(self, input=None):
        """ process a block of input and produces an output """
        raise Exception("This must be implemented in your subclass")

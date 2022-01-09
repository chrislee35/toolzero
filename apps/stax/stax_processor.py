class StaxProcessor:
    INITIALIZED = False
    NAME = 'StaxProcessor'
    # which folder of processors should this processor appear
    # None means that it doesn't appear anywhere
    FOLDER = None # should be str
    # description of the tool
    DESCRIPTION = "Base class for all Stax Processors"

    # list of StaxParameter objects with the parameters to the processor
    PARAMETERS = None
    # input is a list of valid inputs. one of None, 'list', 'string', 'numeric', 'dict', 'generator', 'bytes_generator'
    INPUT_TYPES = None
    # output is one of None, 'list', 'string', 'numeric', 'dict', 'generator', 'bytes_generator'
    OUTPUT_TYPE = None

    def __init__(self, parent):
        self.parent = parent

    def pause(self):
        self.parent.pause()

    def send_output(self, id, message):
        self.parent.send_output(id, message)

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
        raise UnimplementedException("This must be implemented in your subclass")

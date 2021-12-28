class StaxProcessor:
    INITIALIZED = False
    NAME = 'StaxProcessor'
    # which folder of processors should this processor appear
    # None means that it doesn't appear anywhere
    FOLDER = None # should be str

    # list of StaxParameter objects with the parameters to the processor
    PARAMETERS = None
    # input is one of None, 'list', 'scalar', 'dict', 'raw', or 'filename'
    INPUT_TYPE = None
    # output is one of None, 'list', 'scalar', 'dict', 'raw', or 'filename'
    # if you need to ouput a list of filenames, you should use 'list', then
    # use the list to filename looper
    OUTPUT_TYPE = None

    def __init__(self):
        self.ready = False
        self.done = False
        self.output = None

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

    def end_record(self):
        """ this is only used in raw data mode to signify the end of a chunk of data
        this would be often used to end the write to a file or upload """
        pass

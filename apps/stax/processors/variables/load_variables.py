from apps.stax import StaxProcessor, StaxStore
import inspect


class LoadVariables(StaxProcessor):
    INITIALIZED = False
    NAME = 'Load All Variables'
    FOLDER = 'variables'

    PARAMETERS = []
    INPUT_TYPES = ['None']
    OUTPUT_TYPE = 'dict'

    def process(self, params, input):
        active = True
        while active:
            active = False
            base = {}
            for v in StaxStore.variables.keys():
                val = None
                try:
                    val = StaxStore.variables[v].__next__()
                except StopIteration:
                    pass
                base[v] = val
                if val is not None:
                    active = True

            if active:
                yield base

from .stax_processor import StaxProcessor
import types

class StaxEngine:
    INITIALIZED = False
    PROCESSORS = {}

    def __init__(self):
        self.variables = {}
        self.pipeline = []
        if not self.INITIALIZED:
            self._discover_processors()

    def load_pipeline(self, processor_names):
        for pn in processor_names:
            self.append_processor(pn)

    def _discover_processors(self):
        import glob, os
        for p in glob.glob('apps/stax/processors/*'):
            if not os.path.isdir(p):
                continue
            name = p.replace('/', '.')
            mod = __import__(name, fromlist=[''])
            kls = [x for x in dir(mod) if not '_' in x and not x == 'StaxProcessor']
            for kl in kls:
                if kl[0] != kl[0].upper():
                    continue
                #print("Loading mod.%s" % kl)
                klass = eval("mod.%s" % kl)
                if issubclass(klass, StaxProcessor):
                    self.PROCESSORS[klass.NAME] = klass

    def list_processors_with_input(self, input_type):
        matching_processors = []
        for proc_name in self.PROCESSORS.keys():
            in_types = self.PROCESSORS[proc_name].INPUT_TYPES
            if input_type is None and in_types is None:
                matching_processors.append(proc_name)
            elif in_types is not None and input_type in in_types:
                matching_processors.append(proc_name)
        return matching_processors

    def append_processor(self, processor_name):
        if not self.PROCESSORS.get(processor_name):
            raise ValueError("Could not find processor with name: %s" % processor_name)
        kls = self.PROCESSORS[processor_name]
        if kls is None:
            raise ArgumentError("Could not load class for processor: %s -> %s" % (processor_name, self.PROCESSORS[processor_name]))
        instance = kls()
        entry = {
            'name': processor_name,
            'proc': instance,
            'stax_params': instance.get_parameters(),
            'params': {}
        }
        previous_processor_name = "__start__"
        previous_output_type = 'None'
        if len(self.pipeline) > 0:
            previous_output_type = self.pipeline[-1]['proc'].OUTPUT_TYPE
            previous_processor_name = self.pipeline[-1]['name']

        valid = False
        if instance.INPUT_TYPES is None and previous_output_type is None:
            valid = True
        elif instance.INPUT_TYPES is None:
            valid = False
        elif previous_output_type in instance.INPUT_TYPES:
            valid = True

        if not valid:
            valid_input_types = 'None'
            if instance.INPUT_TYPES:
                valid_input_types = ','.join(instance.INPUT_TYPES)
            raise ValueError("Processor %s requires input types %s, but the previous processor, %s, outputs %s" %
                (processor_name, valid_input_types, previous_processor_name, previous_output_type))
        self.pipeline.append( entry )
        return entry

    def set_parameter(self, proc_index, parameter, value):
        entry = self.pipeline(proc_index)
        stax_param = None
        for sp in entry['stax_params']:
            if parameter == sp.name:
                if sp.validate(value):
                    entry[parameter] = value
                    return True
                else:
                    return False
        return False

    def set_variable(self, name, value):
        self.variables[name] = value

    def cli_set_parameters(self):
        for entry in self.pipeline:
            if entry['stax_params'] and len(entry['stax_params']) > 0:
                for sp in entry['stax_params']:
                    valid = False
                    while not valid:
                        value = input('[%s] %s (%s) [%s]: ' % (entry['name'], sp.name, sp.type, sp.default))
                        if not value or len(value) == 0:
                            value = sp.default
                        if sp.validate(value):
                            entry['params'][sp.name] = value
                            valid = True
                        else:
                            print("Try again")

    def run_pipeline(self, start=0, input=None):
        # at this point all the processors should be initalized and all the parameters set
        # we need to run each processor in order.  if the processor returns, then it is done
        # if the processor yields, then this is a "stream" interface, pass the generator to the
        # next processor and let it consume it
        last_output = input
        for i, entry in enumerate(self.pipeline[start:]):
            input = {
                'input': last_output,
                'params': entry['params']
            }
            last_output = entry['proc'].process(input)
            # if generator and output type is scalar, then we are unrolling a loop
            if type(last_output) == types.GeneratorType and entry['proc'].OUTPUT_TYPE not in ['generator', 'bytes_generator']:
                for item in last_output:
                    lo = self.run_pipeline(start+i+1, item)
                last_output = lo
                break # don't run the rest of the pipeline in this call of the function
        return last_output

    def submit_pipeline(self, pipeline, start=0):
        self.pipeline = []
        if start == 0:
            self.variables = {}
        for block in pipeline:
            entry = self.append_processor(block['processor'])
            if len(entry['stax_params']) > 0:
                for sp in entry['stax_params']:
                    entry['params'][sp.name] = block['parameters'][sp.name]
        answer = self.run_pipeline(start)
        yield answer

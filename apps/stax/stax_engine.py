from .stax_processor import StaxProcessor
from .stax_store import StaxStore
import types


class StaxEngine:
    INITIALIZED = False
    PROCESSORS = {}

    def __init__(self, parent=None):
        self.parent = parent
        self.pipeline = []
        if not self.INITIALIZED:
            self._discover_processors()

    def load_pipeline(self, processor_names):
        for pn in processor_names:
            self.append_processor(pn)

    def _discover_processors(self):
        import glob
        import os
        for p in glob.glob('apps/stax/processors/*'):
            if not os.path.isdir(p):
                continue
            name = p.replace('/', '.')
            mod = __import__(name, fromlist=[''])
            kls = [x for x in dir(mod) if '_' not in x and not x == 'StaxProcessor']
            for kl in kls:
                if kl[0] != kl[0].upper():
                    continue
                klass = eval("mod.%s" % kl)
                if issubclass(klass, StaxProcessor):
                    self.PROCESSORS[klass.NAME] = klass

    def append_processor(self, processor_name, output_type):
        if not self.PROCESSORS.get(processor_name):
            raise ValueError("Could not find processor with name: %s" % processor_name)
        kls = self.PROCESSORS[processor_name]
        if kls is None:
            raise Exception("Could not load class for processor: %s -> %s" % (processor_name, self.PROCESSORS[processor_name]))
        instance = kls(self)
        entry = {
            'name': processor_name,
            'proc': instance,
            'stax_params': instance.get_parameters(),
            'params': {}
        }
        previous_output_type = 'None'
        if len(self.pipeline) > 0:
            previous_output_type = self.pipeline[-1]['proc'].get_output_type()

        # set input type may also throw an exception if the input to the instance
        # is incompatible with the processor
        instance.set_input_type(previous_output_type)
        if output_type:
            instance.set_output_type(output_type)
        self.pipeline.append(entry)
        return entry

    def set_parameter(self, proc_index, parameter, value):
        entry = self.pipeline(proc_index)
        for sp in entry['stax_params']:
            if parameter == sp.name:
                if sp.validate(value):
                    entry[parameter] = value
                    return True
                else:
                    return False
        return False

    def set_variable(self, name, value):
        StaxStore.set(name, value)

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
        self.pause = False
        for i, entry in enumerate(self.pipeline[start:]):
            if self.pause:
                return
            last_output = entry['proc'].process(entry['params'], last_output)

        return last_output

    def send_output(self, id, message):
        if self.parent:
            self.parent.send_output(id, message)
        else:
            print("CLI "+message)

    def pause(self):
        self.pause = True

    def submit_pipeline(self, pipeline, start=0):
        self.pipeline = []
        if start == 0:
            StaxStore.clear()
        try:
            for block in pipeline:
                entry = self.append_processor(block['processor'], block.get('output'))
                if block.get('parameters') is None:
                    block['parameters'] = {}
                entry['params']['id'] = block['parameters'].get('id', 'cli')
                for sp in entry['stax_params']:
                    if block['parameters'].get(sp.name):
                        entry['params'][sp.name] = block['parameters'][sp.name]
                    else:
                        entry['params'][sp.name] = sp.default

            return self.run_pipeline(start)
        except Exception as e:
            self.parent.send_error(str(e))

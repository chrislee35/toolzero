from stax import StaxProcessor

class StaxEngine:
    PROCESSORS = {
        'CLI Input Str': 'stax.processors.interact.CLIInputStr',
        'CLI Print Str': 'stax.processors.interact.CLIPrintStr',
        'Template Transform': 'stax.processors.data.TemplateTransform',
        'XOR': 'stax.processors.data.XorStreamProcessor',
        'Copy File': 'stax.processors.file.CopyFileProcessor',
        'Move File': 'stax.processors.file.MoveFileProcessor',
        'Read File': 'stax.processors.file.ReadFileProcessor',
        'Write File': 'stax.processors.file.WriteFileProcessor',
        'DNS': 'stax.processors.web.DnsProcessor',
        'HTTP': 'stax.processors.web.HttpProcessor',
        'REST': 'stax.processors.web.RestProcessor'
    }

    def __init__(self):
        self.pipeline = []

    def load_pipeline(self, processor_names):
        for pn in processor_names:
            self.append_processor(pn)

    def _load_app(self, app_name):
        pathname = '.'.join(app_name.split('.')[0:-1])
        classname = app_name.split('.')[-1]
        mod = __import__(pathname, fromlist=[''])
        klass = eval("mod."+classname)
        if issubclass(klass, StaxProcessor):
            return klass
        return None

    def append_processor(self, processor_name):
        if not self.PROCESSORS.get(processor_name):
            raise ValueError("Could not find processor with name: %s" % processor_name)
        kls = self._load_app(self.PROCESSORS[processor_name])
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
        previous_input_type = None
        if len(self.pipeline) > 0:
            previous_input_type = self.pipeline[-1]['proc'].OUTPUT_TYPE
            previous_processor_name = self.pipeline[-1]['name']
        if instance.INPUT_TYPE != previous_input_type:
            raise ValueError("Processor %s requires input type %s, but the previous processor, %s, outputs %s" %
                (processor_name, instance.INPUT_TYPE, previous_processor_name, previous_input_type))
        self.pipeline.append( entry )

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

    def run_pipeline(self):
        # at this point all the processors should be initalized and all the parameters set
        # we need to run each processor in order.  if the processor returns, then it is done
        # if the processor yields, then this is a "stream" interface, pass the generator to the
        # next processor and let it consume it
        last_output = None
        for i, entry in enumerate(self.pipeline):
            input = {
                'input': last_output,
                'params': entry['params']
            }
            last_output = entry['proc'].process(input)

if __name__ == "__main__":
    se = StaxEngine()
    se.append_processor('CLI Input Str')
    se.append_processor('Read File')
    se.append_processor('XOR')
    se.append_processor('Write File')
    se.append_processor('Copy File')
    se.append_processor('CLI Print Str')

    se.cli_set_parameters()
    se.run_pipeline()

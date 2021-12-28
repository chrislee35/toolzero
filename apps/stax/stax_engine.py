import types

class StaxEngine:
    PROCESSORS = {
        'CLI Input Str': 'stax.processors.interact.CLIInputStr',
        'CLI Print Str': 'stax.processors.interact.CLIPrintStr',
        'Template Transform': 'stax.processors.data.TemplateTransform',
        'Move File': 'stax.processors.file.MoveFileProcessor',
        'Write File': 'stax.processors.file.WriteFileProcessor',
        'DNS': 'stax.processors.web.DnsProcessor',
        'HTTP': 'stax.processors.web.HttpProcessor',
        'REST': 'stax.processors.web.RestProcessor'
    }

    def __init__(self):
        self.pipeline = []

    def load_pipeline(self, processor_names):
        for pn in processor_names:
            if not self.PROCESSORS.get(pn):
                raise ArgumentError("Could not find processor with name: %s" % pn)
            kls = eval('import %s' % self.PROCESSORS[pn])
            instance = kls()
            entry = {
                'name': pn,
                'proc': instance,
                'stax_params': instance.get_parameters(),
                'params': {}
            }
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
        # if the processor yields, then we need to pass each "record" to the next processor,
        # run the next processor, then go back to the yielding processor and run it.
        last_output = None
        for i, entry in enumerate(self.pipeline):
            input = {
                'input': last_output,
                'params': entry['params']
            }
            val = entry['proc'].process(input)
            if type(val) == types.GeneratorType:
                # get the next processor entry in the pipeline to feed
                next_entry = self.pipeline[i+1]
                # read records from the current processor
                for rec in val:
                    subinput = {
                        'input': rec,
                        'params': next_entry['params']
                    }
                    # feed the next process
                    val2 = next_entry['proc'].process(subinput)
                    last_output = val2
            else:
                last_output = val

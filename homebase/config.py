# This module loads a base config and applies updates from custom configurations
import os, inspect, json

def caller_class(skip=2):
    """Get a name of a caller in the format module.class.method

       `skip` specifies how many levels of stack to skip while getting caller
       name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

       An empty string is returned if skipped levels exceed stack height
    """
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
      return ''
    parentframe = stack[start][0]    

    name = []
    module = inspect.getmodule(parentframe)
    # `modname` can be None when frame is executed directly in console
    # TODO(techtonik): consider using __main__
    if module:
        name.append(module.__name__)
    # detect classname
    if 'self' in parentframe.f_locals:
        # I don't know any way to detect call from the object method
        # XXX: there seems to be no way to detect static method call - it will
        #      be just a function call
        name.append(parentframe.f_locals['self'].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != '<module>':  # top level usually
        name.append( codename ) # function or a method

    ## Avoid circular refs and frame leaks
    #  https://docs.python.org/2.7/library/inspect.html#the-interpreter-stack
    del parentframe, stack

    return name[1]

class Config:
    config = None
    filename = None
    needs_saving = False
    
    def __init__(self, config_file=None):
        # the reason that I figure out the calling class name is to try to limit the scope of the calling app to its own 
        # namespace.  If someone got remote access to a given app, it would only be able to access its
        # own variables--at least that the desired effect by the time I finish engineering this.
        # The second reason, is simplicity, you don't have to worry about naming variables in a globally 
        # unique way and from the app developers' point of view, the variable names are shorter.
        self.class_name = caller_class()

        if Config.config:
            return
            
        Config.config = {}
        
        if not config_file and os.environ.get('HOME'):
            config_file = os.environ.get('HOME')+os.sep+'.homebase'
        if config_file and os.path.exists(config_file):
            self.load(config_file)
        
        Config.filename = config_file
        
    def get_dict(self):
        return Config.config.get(self.class_name, {})
        
    def set(self, name, value):
        if not Config.config.get(self.class_name):
            Config.config[self.class_name] = {}
        Config.config[self.class_name][name] = value
        Config.needs_saving = True
        
    def get(self, name, default=None):
        if not Config.config.get(self.class_name):
            return default
        return Config.config[self.class_name].get(name, default)
        
    def load(self, filename):
        with open(filename, 'r') as fh:
            self.load_fh(fh)

    def load_fh(self, fh):
        config = json.load(fh)
        Config.config.update(config)
        if Config.filename:
            Config.needs_saving = True
            
    def save(self, filename=None):
        # if no filename is provided, try the default filename
        if not filename:
            if Config.filename:
                filename = Config.filename
            else:
                return
        
        if filename == Config.filename and not Config.needs_saving:
            return
            
        # make a backup
        if os.path.exists(filename):
            backup = filename+'.bak'
            with open(filename, 'r') as fh:
                with open(backup, 'w') as tofh:
                    tofh.write(fh.read())

        with open(filename, 'w') as fh:
            json.dump(Config.config, fh, indent=4)
            
        if filename == Config.filename:
            Config.needs_saving = False
                
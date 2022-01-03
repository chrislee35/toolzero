import os
import glob

path = os.path.dirname(__file__)
modules = [os.path.basename(f)[:-3] for f in glob.glob(path + "/*.py")
           if not os.path.basename(f).startswith('_')]
stripped_path = os.path.relpath(path).replace('/', '.')
imports = {}
for module in modules:
    model_name = module.title().replace("_", "")
    imports[model_name] = getattr(__import__(stripped_path + "." + module,
        fromlist=[model_name]), model_name)
globals().update(imports)

from homebase import BaseTool
from .stax_engine import StaxEngine
import time, json

class StaxApp(BaseTool):
    def __init__(self):
        self.name = "Stax"
        self.folder = "Test"
        self.engine = StaxEngine()

    def list_processors(self, **kwargs):
        processors = {}
        for proc in self.engine.PROCESSORS:
            p = self.engine.PROCESSORS[proc]
            params = p.PARAMETERS or []
            processors[proc] = {
                'name': proc,
                'folder': p.FOLDER,
                'inputs': p.INPUT_TYPES,
                'output': p.OUTPUT_TYPE,
                'parameters': [ { 'name': x.name, 'type': x.type, 'default': x.default } for x in params ]
            }
        yield self.success(processors)

    def run_pipeline(self, **kwargs):
        for message in self.engine.submit_pipeline(kwargs['pipeline']):
            yield self.success(message)

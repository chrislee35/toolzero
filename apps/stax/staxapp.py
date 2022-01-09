from homebase import BaseTool
from .stax_engine import StaxEngine
import types
from queue import Queue
from threading import Thread

class StaxApp(BaseTool):
    def __init__(self):
        self.name = "Stax"
        self.folder = "Test"
        self.engine = StaxEngine(self)
        self.queue = Queue()

    def list_processors(self, **kwargs):
        print("Listing the processors")
        processors = {}
        for proc in self.engine.PROCESSORS:
            p = self.engine.PROCESSORS[proc]
            params = p.PARAMETERS or []
            processors[proc] = {
                'name': proc,
                'folder': p.FOLDER,
                'inputs': p.INPUT_TYPES,
                'output': p.OUTPUT_TYPE,
                'parameters': [x.to_data() for x in params]
            }
        yield self.success(processors)

    def run_pipeline(self, **kwargs):
        start = int(kwargs.get('start', 0))
        pipeline = kwargs['pipeline']
        t = Thread(target=self.submit_pipeline, args=(pipeline, start))
        t.start()
        message = self.queue.get()
        while message:
            if isinstance(message, types.GeneratorType):
                for item in message:
                    yield self.success(item)
            else:
                yield self.success(message)
            message = self.queue.get()

        t.join()

    def submit_pipeline(self, pipeline, start):
        for message in self.engine.submit_pipeline(pipeline, start):
            self.queue.put(message)
        self.queue.put(None)

    def send_output(self, id, message):
        item = {'type': 'output', 'id': id, 'message': message}
        self.queue.put(item)

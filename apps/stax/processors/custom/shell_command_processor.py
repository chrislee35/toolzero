from apps.stax import StaxProcessor, StaxParameter
import shlex
import sys
from subprocess import PIPE, Popen
from threading import Thread
from queue import Queue, Empty

ON_POSIX = 'posix' in sys.builtin_module_names


class ShellCommandProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Shell Command'
    FOLDER = 'custom'

    PARAMETERS = [
        StaxParameter('command', 'string', '/usr/bin/uuencode --base64')
    ]
    INPUT_TYPES = ['generator']
    OUTPUT_TYPE = 'generator'

    def enqueue_output(self, out, queue):
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()

    def process(self, input):
        cmd = shlex.split(input['params']['command'])
        subproc = Popen(cmd,
            bufsize=1,
            close_fds=ON_POSIX,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            universal_newlines=True
        )
        que = Queue()
        t = Thread(target=self.enqueue_output, args=(subproc.stdout, que))
        t.daemon = True
        t.start()

        for item in input['input']:
            subproc.stdin.write(item)
            while True:
                try:
                    line = que.get(timeout=0.1)
                except Empty:
                    break
                else:
                    yield line
        subproc.stdin.close()
        t.join()
        while True:
            try:
                line = que.get(timeout=0.1)
            except Empty:
                break
            else:
                yield line

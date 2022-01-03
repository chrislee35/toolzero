from apps.stax import StaxProcessor, StaxParameter
import ast
import math


class MathFormulaProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Math Formula'
    FOLDER = 'custom'

    PARAMETERS = [
        StaxParameter('code', 'textbox', 'x + pi')
    ]
    INPUT_TYPES = ['numeric']
    OUTPUT_TYPE = 'numeric'

    SAFE_DICT = None

    def __init__(self):
        if not self.INITIALIZED:
            safe_list = ['acos', 'asin', 'atan', 'atan2', 'ceil', 'cos',
                 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor',
                 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10',
                 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt',
                 'tan', 'tanh']

            # creating a dictionary of safe methods
            self.SAFE_DICT = dict([(k, getattr(math, k)) for k in safe_list])

    def process(self, input):
        code = input['params']['code']
        block = ast.parse(code, mode='exec')
        last = ast.Expression(block.body.pop().value)

        item = input['input']
        _globals, _locals = {}, {'x': item}
        _locals.update(self.SAFE_DICT)
        exec(compile(block, '<string>', mode='exec'), _globals, _locals)
        return eval(compile(last, '<string>', mode='eval'), _globals, _locals)

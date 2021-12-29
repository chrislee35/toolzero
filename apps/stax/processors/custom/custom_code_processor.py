from stax import StaxProcessor, StaxParameter
import ast

class CustomCodeProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Custom Code'
    FOLDER = 'custom'

    PARAMETERS = [
        StaxParameter('code', 'textbox', 'x = b\'hello \'+item\nx + x')
    ]
    INPUT_TYPE = 'stream'
    OUTPUT_TYPE = 'stream'

    def process(self, input):
        code = input['params']['code']
        block = ast.parse(code, mode='exec')
        last = ast.Expression(block.body.pop().value)

        for item in input['input']:
            _globals, _locals = {}, {'item': item}
            exec(compile(block, '<string>', mode='exec'), _globals, _locals)
            yield eval(compile(last, '<string>', mode='eval'), _globals, _locals)

# def exec_then_eval(code):
#     block = ast.parse(code, mode='exec')
#     # assumes last node is an expression
#     last = ast.Expression(block.body.pop().value)
#     _globals, _locals = {}, {}
#     exec(compile(block, '<string>', mode='exec'), _globals, _locals)
#     return eval(compile(last, '<string>', mode='eval'), _globals, _locals)

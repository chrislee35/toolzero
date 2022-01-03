from apps.stax import StaxProcessor, StaxParameter
import ast


class CustomCodeProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Custom Code'
    FOLDER = 'custom'

    PARAMETERS = [
        StaxParameter('code', 'textbox', 'x = \'hello \'+item\nx + x')
    ]
    INPUT_TYPES = ['generator']
    OUTPUT_TYPE = 'generator'

    def process(self, input):
        code = input['params']['code']
        block = ast.parse(code, mode='exec')
        last = ast.Expression(block.body.pop().value)

        for item in input['input']:
            _globals, _locals = {}, {'item': item}
            exec(compile(block, '<string>', mode='exec'), _globals, _locals)
            yield eval(compile(last, '<string>', mode='eval'), _globals,
                _locals)

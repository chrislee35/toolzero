from apps.stax import StaxProcessor, StaxParameter, ComboboxParameter
import ast


class CustomCodeProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Custom Code'
    FOLDER = 'custom'

    PARAMETERS = [
        StaxParameter('code', 'textbox', 'x = \'hello \'+item\nx + x')
    ]
    INPUT_TYPES = ['string', 'numeric', 'dict', 'list(string)', 'list(numeric)', 'list(dict)', 'bytes']
    OUTPUT_TYPE = 'select'
    OUTPUT_TYPES = ['string', 'numeric', 'dict', 'list(string)', 'list(numeric)', 'list(dict)', 'bytes']

    def process(self, params, input):
        code = params['code']
        block = ast.parse(code, mode='exec')
        last = ast.Expression(block.body.pop().value)

        for item in input:
            _globals, _locals = {}, {'item': item}
            exec(compile(block, '<string>', mode='exec'), _globals, _locals)
            yield eval(compile(last, '<string>', mode='eval'), _globals,
                _locals)

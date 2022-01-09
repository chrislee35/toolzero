from apps.stax import StaxProcessor, StaxParameter, ComboboxParameter
import ast


class CustomCodeProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Custom Code'
    FOLDER = 'custom'

    PARAMETERS = [
        ComboboxParameter('output type', ['string', 'numeric', 'dict'], 'string'),
        StaxParameter('code', 'textbox', 'x = \'hello \'+item\nx + x')
    ]
    INPUT_TYPES = ['string', 'numeric', 'dict']
    OUTPUT_TYPE = 'select'

    def process(self, params, input):
        code = params['code']
        block = ast.parse(code, mode='exec')
        last = ast.Expression(block.body.pop().value)

        for item in input:
            _globals, _locals = {}, {'item': item}
            exec(compile(block, '<string>', mode='exec'), _globals, _locals)
            yield eval(compile(last, '<string>', mode='eval'), _globals,
                _locals)

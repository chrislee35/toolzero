from apps.stax import StaxProcessor, StaxParameter, ComboboxParameter
import random


class SortProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Sort'
    FOLDER = 'data'

    PARAMETERS = [
        ComboboxParameter('sort type', ['dictionary', 'numeric', 'random'],
            'dictionary'),
        StaxParameter('reverse', 'boolean', False),
        StaxParameter('unique', 'boolean', False)
    ]
    INPUT_TYPES = ['list', 'generator']
    OUTPUT_TYPE = 'list'

    def process(self, input):
        sort_type = input['params']['sort type']
        reverse = input['params']['reverse']
        unique = input['params']['unique']

        if type(input['input']) != list:
            input['input'] = list(input['input'])

        if unique:
            input['input'] = list(set(input['input']))

        if sort_type == 'numeric':
            return sorted(input['input'], key=SortProcessor.numeric_sort,
                reverse=reverse)
        elif sort_type == 'random':
            return random.sample(input['input'], len(input['input']))
        else:
            return sorted(input['input'], reverse=reverse)

    @staticmethod
    def numeric_sort(x):
        if type(x) == str:
            return (len(x), x)
        elif type(x) in [int, float, complex]:
            return x
        else:
            raise Exception("Cannot numerically sort objects of type: %s" %
                str(type(x)))

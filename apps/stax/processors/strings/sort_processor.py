from apps.stax import StaxProcessor, StaxParameter, ComboboxParameter
import random


class SortProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Sort'
    FOLDER = 'strings'

    PARAMETERS = [
        ComboboxParameter('sort type', ['dictionary', 'numeric', 'random'],
            'dictionary'),
        StaxParameter('reverse', 'boolean', False),
        StaxParameter('unique', 'boolean', False)
    ]
    INPUT_TYPES = ['list(string)', 'list(numeric)']
    OUTPUT_TYPE = 'input'

    def process(self, params, input):
        sort_type = params['sort type']
        reverse = params['reverse']
        unique = params['unique']

        for input_list in input:
            if unique:
                input_list = list(set(input_list))
            if sort_type == 'numeric':
                yield sorted(input_list, key=SortProcessor.numeric_sort, reverse=reverse)
            elif sort_type == 'random':
                yield random.sample(input_list, len(input_list))
            else:
                yield sorted(input_list, reverse=reverse)

    @staticmethod
    def numeric_sort(x):
        if type(x) == str:
            return (len(x), x)
        elif type(x) in [int, float, complex]:
            return x
        else:
            raise Exception("Cannot numerically sort objects of type: %s" %
                str(type(x)))

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
    INPUT_TYPES = ['string', 'numeric']
    OUTPUT_TYPE = 'input'

    def process(self, params, input):
        sort_type = params['sort type']
        reverse = params['reverse']
        unique = params['unique']

        if type(input) != list:
            input = list(input)

        if unique:
            input = list(set(input))

        if sort_type == 'numeric':
            for item in sorted(input, key=SortProcessor.numeric_sort,
                reverse=reverse):
                yield item
        elif sort_type == 'random':
            for item in random.sample(input, len(input)):
                yield item
        else:
            for item in sorted(input, reverse=reverse):
                yield item

    @staticmethod
    def numeric_sort(x):
        if type(x) == str:
            return (len(x), x)
        elif type(x) in [int, float, complex]:
            return x
        else:
            raise Exception("Cannot numerically sort objects of type: %s" %
                str(type(x)))

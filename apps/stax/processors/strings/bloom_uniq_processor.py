from apps.stax import StaxProcessor, StaxParameter
import hashlib


# repurposed from https://dev.to/anarchyrucks/
# implementing-a-simple-bloom-filter-in-python-11bh
class SimpleBloomFilter:
    def __init__(self, length):
        self.len = length
        self.filter = bytearray(length)

    def bytes_to_int(self, hash_value):
        return int.from_bytes(hash_value, byteorder='big')

    def bloom_index(self, hashint):
        return hashint % self.len

    def fill_percentage(self):
        return self.filter.count(1) / self.len * 100

    def check_indices(self, indices):
        new = False
        for i in indices:
            byte_i = int(i / 8)
            bit_i = i % 8
            if self.filter[byte_i] >> bit_i & 1 == 0:
                new = True
                break
        return new

    def set_indices(self, indices):
        for i in indices:
            byte_i = int(i / 8)
            bit_i = i % 8
            self.filter[byte_i] = self.filter[byte_i] | 1 << bit_i

    def item_to_indicies(self, item):
        m1 = hashlib.md5()
        m2 = hashlib.sha1()
        m3 = hashlib.sha224()
        item = item.encode('UTF-8')

        m1.update(item)
        m2.update(item)
        m3.update(item)

        hash_values = [m1.digest(), m2.digest(), m3.digest()]
        hashints = list(map(self.bytes_to_int, hash_values))
        indices = list(map(self.bloom_index, hashints))
        return indices

    def check(self, item):
        indices = self.item_to_indicies(item)
        return self.check_indices(indices)

    def set(self, item):
        indicies = self.item_to_indicies(item)
        self.set_indices(indicies)

    def check_and_set(self, item):
        indicies = self.item_to_indicies(item)
        n = self.check_indices(indicies)
        if n:
            self.set_indices(indicies)
        return n


class BloomUniqProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'Bloom Filter Uniq'
    FOLDER = 'strings'

    PARAMETERS = [
        StaxParameter('bloom filter size (bytes)', 'number', 64*1024)
    ]
    INPUT_TYPES = ['string', 'number']
    OUTPUT_TYPE = 'input'

    def process(self, params, input):
        bloom_size = params['bloom filter size (bytes)']

        filter = SimpleBloomFilter(bloom_size)
        for item in input:
            if filter.check_and_set(str(item)):
                yield item

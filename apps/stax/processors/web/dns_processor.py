import socket
from apps.stax import StaxProcessor

class DnsProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'DNS'
    # which folder of processors should this processor appear
    # None means that it doesn't appear anywhere
    FOLDER = 'web' # should be str

    # list of StaxParameter objects with the parameters to the processor
    PARAMETERS = []
    # input is a single hostname
    INPUT_TYPES = ['string']
    # output is the ip
    OUTPUT_TYPE = 'string'

    def process(self, input):
        hostname = input['input']
        if hostname:
            host = socket.gethostbyname(hostname)
            return host
        else:
            return None

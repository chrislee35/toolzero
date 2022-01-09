import socket
from apps.stax import StaxProcessor


class DnsProcessor(StaxProcessor):
    INITIALIZED = False
    NAME = 'DNS Resolve'
    FOLDER = 'web'

    PARAMETERS = []
    INPUT_TYPES = ['string']
    OUTPUT_TYPE = 'string'

    def process(self, params, input):
        for hostname in input:
            host = socket.gethostbyname(hostname)
            yield host

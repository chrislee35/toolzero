from homebase import BaseTool
import json
import urllib3


class TestTableApp(BaseTool):
    def __init__(self, parent):
        self.name = "Test Table"
        self.folder = "Test"
        self.parent = parent
        self.data = {}
        self.fields = [
            {
                'label': 'URL',
                'key': 'url',
                'type': 'text',
                'default': '',
                'onchange': 'fetch_data'
            }
        ]

        self.result_type = {
            'type': 'table'
        }

    def fetch_data(self, url, **kwargs):
        http = urllib3.PoolManager()
        headers = kwargs.get('headers', {'Accept': 'application/json'})

        r = http.request(
            'GET',
            url,
            headers=headers
        )
        data = json.loads(r.data.decode('utf-8'))
        col_header = list(data[0].keys())
        yield self.success(col_header, progress=0)
        for i, p in enumerate(data):
            row = []
            for c in col_header:
                row.append(p.get(c, ''))
            yield self.success(row, progress=int(100*(i+1)/len(data)))

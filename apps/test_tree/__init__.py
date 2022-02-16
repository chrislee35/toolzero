from homebase import BaseTool
import json
import urllib3


class TestTreeApp(BaseTool):
    def __init__(self, parent):
        self.name = "Test Tree"
        self.folder = "Test"
        self.parent = parent
        self.data = {}
        self.fields = [
            {
                'label': 'URL',
                'key': 'url',
                'type': 'text',
                'default': 'https://www.chrisleephd.us/stuff/presidents.json'
            },
            {
                'type': 'button',
                'text': 'Submit',
                'onclick': 'fetch_data'
            }
        ]

        self.result_type = {
            'type': 'tree',
            'callback': 'register_choice'
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
        tree_data = {}
        for d in data:
            key = d['name']+'-'+str(d['number'])
            tree_data[key] = d
        yield self.success(tree_data, 100)

    def register_choice(self, data, **kwargs):
        print("Tree item chosen: "+data)
        yield self.success(data, 100)

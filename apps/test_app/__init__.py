from homebase import BaseTool
import time


class TestApp(BaseTool):
    def __init__(self, parent):
        self.name = "Test App"
        self.folder = "Test"
        self.parent = parent
        self.data = {}
        self.fields = [
            {
                'label': 'Name',
                'key': 'name',
                'type': 'text',
                'default': '',
                'onchange': 'check_name'
            },
            {
                'label': 'Age',
                'key': 'age',
                'type': 'list',
                'values': ['1-10', '11-20', '21-30', '31-40'],
                'default': '21-30'
            },
            {
                'label': 'Count',
                'key': 'count',
                'type': 'text',
                'default': '10'
            },
            {
                'type': 'button',
                'text': 'Submit',
                'onclick': 'remember_name_and_age'
            },
            {
                'type': 'button',
                'text': 'Count',
                'onclick': 'count_up'
            }
        ]

        self.result_type = {
            'type': 'textarea',
            'default': 'Results will show here'
        }

    def check_name(self, name, **kwargs):
        if len(name) < 5:
            return self.error('Name too short.')
        elif self.data.get(name):
            return self.error('Name already taken.')
        else:
            return self.success('Nice name!')

    def remember_name_and_age(self, name, age, **kwargs):
        self.data[name] = age
        yield self.success('I will remember you.', progress=50)
        time.sleep(5)
        yield self.success('finished', progress=75)

    def count_up(self, count=10, **kwargs):
        count = int(count)
        for i in range(count):
            yield(self.success(str(i), progress=(i+1)*100/count))
            time.sleep(1)

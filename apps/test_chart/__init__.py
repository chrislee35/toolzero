from homebase import BaseTool


class TestChartApp(BaseTool):
    def __init__(self, parent):
        self.name = "Test Chart"
        self.folder = "Test"
        self.parent = parent
        self.data = {}
        self.fields = [
            {
                'type': 'button',
                'text': 'Load Chart',
                'onclick': 'fetch_data'
            }
        ]

        self.result_type = {
            'type': 'chart',
            'callback': 'register_choice'
        }

    def fetch_data(self, **kwargs):
        chart_data = {
            'type': 'bar',
            'data': {
                'labels': ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
                'datasets': [{
                    'label': '# of Votes',
                    'data': [12, 19, 3, 5, 2, 3],
                    'backgroundColor': [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    'borderColor': [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    'borderWidth': 1
                }]
            },
            'options': {
                'scales': {
                    'y': {
                        'beginAtZero': True
                    }
                }
            }
        }
        yield self.success(chart_data, 100)

    def register_choice(self, data, **kwargs):
        print("Chart item chosen: "+data)
        yield self.success(data, 100)

from homebase import BaseTool


class TestGraphApp(BaseTool):
    def __init__(self, parent):
        self.name = "Test Tree"
        self.folder = "Test"
        self.parent = parent
        self.data = {}
        self.fields = [
            {
                'type': 'button',
                'text': 'Load Graph',
                'onclick': 'fetch_data'
            }
        ]

        self.result_type = {
            'type': 'graph',
            'callback': 'register_choice'
        }

    def fetch_data(self, **kwargs):
        graph_data = {
            'nodes': [
                {'id': 1, 'label': "node\none", 'shape': "box", 'color': "#97C2FC"},
                {'id': 2, 'label': "node\ntwo", 'shape': "circle", 'color': "#FFFF00"},
                {'id': 3, 'label': "node\nthree", 'shape': "diamond", 'color': "#FB7E81"},
                {
                  'id': 4,
                  'label': "node\nfour",
                  'shape': "dot",
                  'size': 10,
                  'color': "#7BE141",
                },
                {'id': 5, 'label': "node\nfive", 'shape': "ellipse", 'color': "#6E6EFD"},
                {'id': 6, 'label': "node\nsix", 'shape': "star", 'color': "#C2FABC"},
                {'id': 7, 'label': "node\nseven", 'shape': "triangle", 'color': "#FFA807"},
                {
                  'id': 8,
                  'label': "node\neight",
                  'shape': "triangleDown",
                  'color': "#6E6EFD",
                },
            ],
            'edges': [
                {'from': 1, 'to': 8, 'arrows': 'to', 'color': {'color': "red"}},
                {'from': 1, 'to': 3, 'color': "rgb(20,24,200)"},
                {
                  'from': 1,
                  'to': 2,
                  'color': {'color': "rgba(30,30,30,0.2)", 'highlight': "blue"},
                },
                {'from': 2, 'to': 4, 'arrows': 'to', 'dashes': True, 'color': {'inherit': "to"}},
                {'from': 2, 'to': 5, 'color': {'inherit': "from"}},
                {'from': 5, 'to': 6, 'color': {'inherit': "both"}},
                {'from': 6, 'to': 7, 'color': {'color': "#ff0000", 'opacity': 0.3}},
                {'from': 6, 'to': 8, 'color': {'opacity': 0.3}},
            ],
            'options': {
                'nodes': {
                    'shape': 'circle',
                    'font': {
                        'size': 15,
                        'color': "black",
                        'face': "courier",
                        'strokeWidth': 3,
                        'strokeColor': "#ffffff",
                    },
                }
            }
        }
        yield self.success(graph_data, 100)

    def register_choice(self, data, **kwargs):
        print("Graph node chosen: "+data)
        yield self.success(data, 100)

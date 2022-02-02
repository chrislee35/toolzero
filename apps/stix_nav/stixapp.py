from homebase import BaseTool
import stix2
import zipfile
import json
import glob


class StixApp(BaseTool):
    instance_memstore = None

    def __init__(self):
        self.name = "STIX Navigator"
        self.folder = "STIX"
        self.memstore = StixApp.instance_memstore
        self.valid_sources = ['mitre-attack']
        self.valid_types = [
            "attack-pattern", "course-of-action",
            "identity", "intrusion-set", "malware", "marking-definition",
            "relationship", "tool", "x-mitre-collection", "x-mitre-data-component",
            "x-mitre-data-source", "x-mitre-matrix", "x-mitre-tactic"
        ]

    def load_stix_file(self, filename, **kwargs):
        if not self.memstore:
            self.memstore = stix2.MemoryStore()
            self.memstore.load_from_file(filename)
        yield self.success(self.valid_types)

    def get_type(self, entity_type, **kwargs):
        filter = stix2.Filter("type", "=", entity_type)
        res = self.memstore.query([filter])
        matches = []
        for ap in res:
            external_id = None
            for er in ap.get('external_references', []):
                if er['source_name'] in self.valid_sources:
                    external_id = er['external_id']
                    break
            if not external_id:
                external_id = ap['name']
            matches.append([ap['id'], ap['name'], external_id])
        yield self.success(matches)

    def get_details(self, id, **kwargs):
        item = self.memstore.get(id)
        if not item:
            yield self.error("Could not find entity with id")
        yield self.success(json.loads(item.serialize()))

    def get_relationships(self, id, **kwargs):
        item = self.memstore.get(id)
        if not item:
            yield self.error("Could not find entity with id")
        yield self.success([json.loads(x.serialize()) for x in self.relationships(item)])

    def get_shape_and_color_for_type(self, etype):
        if etype == 'intrusion-set':
            return('box', 'red')
        else:
            return('box', 'gray')

    def get_colors_for_relationship(self, relationship_type):
        if relationship_type == 'uses':
            return('blue', 'white')
        else:
            return('black', 'gray')

    def get_relationship_graph(self, id, hops, **kwargs):
        item = self.memstore.get(id)
        if not item:
            yield self.error("Could not find entity with id")
        rels = self.memstore.relationships(item)
        node_refs = list(set([x['target_ref'] for x in rels] + [x['source_ref'] for x in rels]))
        node_names = [(self.memstore.get(x)['name'], self.memstore.get(x)['type']) for x in node_refs]
        # TODO: expand relationship #hops out.
        nodes = []
        for idx, rec in enumerate(node_names):
            name, etype = rec
            shape, color = self.get_shape_and_color_for_type(etype)
            nodes.append({'id': idx, 'label': name, 'shape': shape, 'color': color})

        edges = []
        for rel in rels:
            sidx = node_refs.index(rel['source_ref'])
            tidx = node_refs.index(rel['target_ref'])
            label = rel['relationship_type']
            line_color, font_color = self.get_colors_for_relationship(label)
            edges.append({'from': sidx, 'to': tidx,  'label': label, 'arrows': 'to', 'font': {'strokeColor': font_color}, 'color': {'color': line_color}})

        graph = {
            'nodes': nodes,
            'edges': edges,
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
        yield self.success(graph, 100)

    def export_website(self, **kwargs):
        filename = 'stix_website.zip'
        zf = zipfile.ZipFile(filename, mode='w', compression=zipfile.ZIP_DEFLATED, compresslevel=5)
        for fn in glob.glob('apps/stix_nav/html/*'):
            zf.write(fn, arcname=fn.replace('apps/stix_nav/', ''))
        for vtype in self.valid_types:
            filter = stix2.Filter("type", "=", vtype)
            res = self.memstore.query([filter])
            matches = []
            for ap in res:
                external_id = None
                for er in ap['external_references']:
                    if er['source_name'] in self.valid_sources:
                        external_id = er['external_id']
                        break
                if external_id:
                    matches.append([ap['id'], ap['name'], external_id])
                    zf.append('id/'+ap['id']+'.json', json.dumps(ap))
            zf.writestr("type/"+vtype+".json", json.dumps(matches))

        yield self.success('Wrote website to '+filename)

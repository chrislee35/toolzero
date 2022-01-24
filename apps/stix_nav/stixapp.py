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

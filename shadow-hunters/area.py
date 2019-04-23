# area.py
# Implements a Area.


class Area:
    def __init__(self, name, desc, domain, action, resource_id):
        self.name = name
        self.desc = desc
        self.zone = None
        self.domain = domain
        self.action = action
        self.resource_id = resource_id

    def getAdjacent(self):
        return [a for a in self.zone.areas if a != self][0]

    def dump(self):
        return {
            'name': self.name,
            'desc': self.desc,
            'domain': str(self.domain)
        }

    def __str__(self):
        return str(self.dump())

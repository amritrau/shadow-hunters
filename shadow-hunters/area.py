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

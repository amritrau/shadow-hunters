from area import Area

# zone.py
# Implements a Zone, which contains two areas.


class Zone:
    def __init__(self, areas):
        # Make sure a list is passed to areas
        if not isinstance(areas, list):
            raise ValueError("areas must be a list.")

        if not len(areas) == 2:
            raise ValueError("len(areas) must equal 2.")

        self.areas = areas

        # Make sure every area in self.areas is an Area object
        for c in self.areas:
            if not isinstance(c, Area):
                raise ValueError("One or more areas is not an Area object.")

    def dump(self):
        return [a.dump() for a in self.areas]

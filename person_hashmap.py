class PersonHashmap:
    def __init__(self, neighbour_range):
        self.people = {}
        self.neighbour_range = neighbour_range
        self.person_count = 0

    def add(self, person, pos):
        div_pos = pos // self.neighbour_range
        coord = (div_pos.x, div_pos.y)
        if coord in self.people:
            self.people[coord].append(person)
        else:
            self.people[coord] = [person]

        self.person_count += 1

    def get(self, pos):
        div_pos = pos // self.neighbour_range
        coord = (div_pos.x, div_pos.y)
        if coord in self.people:
            return self.people[coord]
        else:
            return []

    def remove(self, person, pos):
        div_pos = pos // self.neighbour_range
        coord = (div_pos.x, div_pos.y)
        if coord in self.people and person in self.people[coord]:
            self.people[coord].remove(person)
            self.person_count -= 1

    def move(self, person, from_, to):
        self.remove(person, from_)
        self.add(person, to)

    def __iter__(self):
        for pos in self.people:
            yield from self.people[pos]

    def __len__(self):
        return self.person_count

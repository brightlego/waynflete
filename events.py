class Clock:
    def __init__(self):
        self.time = 0

    def tick(self):
        self.time += 1

    def read(self):
        return self.time


class Schedule:
    def __init__(self, clock):
        self.clock = clock
        self.events = {}

    def register(self, event, time_until):
        if time_until == float("inf") or time_until == float("-inf"):
            return
        time_until = int(time_until)
        time = self.clock.read() + time_until
        if time in self.events:
            self.events[time].append(event)
        else:
            self.events[time] = [event]

    def update(self):
        if self.clock.read() not in self.events:
            return

        for event in self.events[self.clock.read()]:
            event.act()
        del self.events[self.clock.read()]


class Event:
    def __init__(self):
        pass

    def act(self):
        pass


class InfectEvent(Event):
    def __init__(self, infection, target):
        self.infection = infection
        self.target = target
        super().__init__()

    def act(self):
        self.infection.infect(self.target)
        super().act()


class CureEvent(Event):
    def __init__(self, infection, person):
        self.infection = infection
        self.person = person
        super().__init__()

    def act(self):
        self.person.cure(self.infection)
        super().act()


class DeimuniseEvent(Event):
    def __init__(self, imunisations, infection):
        self.imunisations = imunisations
        self.infection = infection
        super().__init__()

    def act(self):
        self.imunisations.deimunise(self.infection)
        super().act()

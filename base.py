import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

NEIGHBOUR_RANGE = 5

def randrange(hrange, centre=0):
    return (random.random()*2 - 1)*hrange + centre

#Integer division but for floats as well
def closest_mul(a, b):
    return (a - a%b)/b

class Vector2D(np.ndarray):
    Xs = ["x", "X"]
    Ys = ["y", "Y"]

    def __new__(cls, x=0, y=0):
        return super().__new__(cls, (2,))

    def __init__(self, x=0, y=0):
        self[0] = x
        self[1] = y

    def __abs__(self):
        return np.sqrt(self[0]**2 + self[1]**2)

    def __getattr__(self, attr):
        if attr in Vector2D.Xs:
            return self[0]
        elif attr in Vector2D.Ys:
            return self[1]
        else:
            return super().__getattr__(attr)

    def __setattr__(self, attr, value):
        if attr in Vector2D.Xs:
            self[0] = value
        elif attr in Vector2D.Ys:
            self[1] = value
        else:
            super().__setattr__(attr, value)

    def __repr__(self):
        return f"Vector2D ({self[0]},{self[1]})"

    def to_string(self, dp=10):
        return f"({round(self[0],dp)},{round(self[1],dp)})"

class BaseInfection:
    RECOVER_TIME = 15
    RECOVER_STANDARD_DEV = 3.5
    INFECT_SUCCESS_CHANCE = 1
    DEIMUNISE_CHANCE = 0

    global_R = {}

    @classmethod
    def get_R(cls):
        total = 0
        for i in cls.global_R:
            total += cls.global_R[i]

        print(total)
        if len(cls.global_R) == 0:
            return 1

        return total / len(cls.global_R)

    @classmethod
    def update_cls(cls):
        cls.global_R = {}

    def __init__(self):
        self.time_infected = 0
        self.infected_count = 0

    def update(self):
        self.time_infected += 1

    def is_cured(self):
        if self.time_infected > random.gauss(self.RECOVER_TIME, self.RECOVER_STANDARD_DEV):
            self.global_R[self] = self.infected_count
            return True
        else:
            return False

    def __init_subclass__(cls):
        cls.global_R = {}

    def infect(self, person):
        if random.random() < self.INFECT_SUCCESS_CHANCE:
            success = person.infect_with(type(self))
            if success:
                self.infected_count += 1

    def __str__(self):
        return type(self).__name__

    def __repr__(self):
        return super().__repr__()

class Imunisations(set):
    def check_deimunises(self):
        infections_to_remove = set()
        for infection in self:
            if random.random() < infection.DEIMUNISE_CHANCE:
                infections_to_remove.add(infection)

        self -= infections_to_remove

class Person:
    def __init__(self, model, x, y):
        self.pos = Vector2D(x, y)
        self.infections = set()
        self.infections_to_add = set()
        self.to_be_cured = set()
        self.imunisations = Imunisations()
        self.model = model

    def distance(self, other):
        if isinstance(other, Person):
            return abs(self.pos - other.pos)
        elif isinstance(other, Vector2D):
            return abs(self.pos - other)
        else:
            return np.inf

    def move(self):
        pass

    def infect(self, other):
        for infection in self.infections:
            infection.infect(other)

    def infect_with(self, Infection):
        for infection in self.infections:
            if isinstance(infection, Infection):
                return False

        for infection in self.imunisations:
            if isinstance(infection, Infection):
                return False

        for infection in self.infections_to_add:
            if isinstance(infection, Infection):
                return False

        self.infections_to_add.add(Infection())
        self.model.person_infected(Infection)
        return True

    def check_cures(self):
        to_be_cured = set()
        for infection in self.infections:
            if infection.is_cured():
                to_be_cured.add(infection)

        return to_be_cured

    def cure(self, to_be_cured):
        self.infections -= to_be_cured
        self.imunisations = self.imunisations | to_be_cured
        self.model.person_cured(to_be_cured)

    def update(self):
        if len(self.infections) > 0:
            for person in self.get_neighbours():
                self.infect(person)

        for infection in self.infections:
            infection.update()

        self.to_be_cured = self.check_cures()

    def finalise_update(self):
        self.infections = self.infections | self.infections_to_add
        self.cure(self.to_be_cured)
        self.move()
        self.infections_to_add -= self.infections_to_add

    def get_neighbours(self):
        return self.model.get_people_around(self.pos)

    def __repr__(self):
        name = "Person"
        if __name__ != "__main__":
            name = __name__+"."+name

        if len(self.infections) == 0:
            return f"<{name} at {self.pos.to_string(3)}>"
        else:
            infection_str = [str(infection) for infection in self.infections]
            infection_str = ', '.join(infection_str)

            return f"<{name} ({infection_str}) at {self.pos.to_string(3)}>"


class BaseModel:
    class Data:
        def __init__(self, t=0):
            self.r_value = [0]*(t+1)
            self.infected_count = [0]*(t+1)

        def add_new_row(self):
            self.r_value.append(0)
            self.infected_count.append(self.infected_count[-1])

    def __init__(self, person_count, person_type=Person, hwidth=100, hheight=100, neighbour_range=NEIGHBOUR_RANGE, gran=NEIGHBOUR_RANGE):
        self.NEIGHBOUR_RANGE = neighbour_range
        self.gran = gran

        self.hwidth = hwidth
        self.hheight = hheight

        self.person_type = person_type

        self.people = np.ndarray(person_count,dtype=person_type)

        for person in range(person_count):
            self.people[person] = person_type(self, randrange(hwidth), randrange(hheight))

        self.init_display()

        self.data = {}
        self.t = 0
        self.register_infection("All")

    def __iter__(self):
        return iter(self.people)

    def register_infection(self, infection):
        self.data[infection] = self.Data(self.t)

    def get_random_person(self):
        return random.choice(self.people)

    def get_people_around(self, pos):
        pass

    def get_people_between(self, bl, tr):
        pass

    def person_infected(self, infection):
        if isinstance(infection, BaseInfection):
            infection_type = type(infection)
        else:
            infection_type = infection
        if infection_type not in self.data:
            self.register_infection(infection_type)

        self.data["All"].infected_count[-1] += 1
        self.data[infection_type].infected_count[-1] += 1


    def person_cured(self, infections):
        for infection in infections:
            if isinstance(infection, BaseInfection):
                infection_type = type(infection)
            else:
                infection_type = infection
            self.data["All"].infected_count[-1] -= 1
            self.data[infection_type].infected_count[-1] -= 1

    def update(self, t, display=True):
        for infection in self.data:
            self.data[infection].add_new_row()
            if isinstance(infection, type) and issubclass(infection, BaseInfection):
                infection.update_cls()

        if display:
            self.update_display()

        for person in self.people:
            person.update()

        for person in self.people:
            person.finalise_update()

        for infection in self.data:
            if infection != 'All':
                self.data[infection].r_value[-1] = infection.get_R()

        self.t += 1
        #return self.r_plot[0]

    def init_display(self):
        X, Y, data = self.get_heatmap_data(gran=self.gran)#self.NEIGHBOUR_RANGE)

        heatmap_fig, heatmap_ax = plt.subplots()
        #r_plot_fig, r_plot_ax = plt.subplots()

        self.heatmap_fig = heatmap_fig
        self.heatmap_ax = heatmap_ax
        self.heatmap = heatmap_ax.pcolormesh(X, Y, data, shading="auto", vmin=0, vmax=1)

        #self.r_plot_fig = r_plot_fig
        #self.r_plot_ax = r_plot_ax
        #self.r_plot = r_plot_ax.plot([])

    def get_heatmap_data(self, gran=NEIGHBOUR_RANGE, infection_type=None):
        x = np.arange(-self.hwidth,self.hwidth,gran)
        y = np.arange(-self.hheight,self.hheight,gran)
        Y, X = np.meshgrid(y, x)
        person_count = np.zeros(Y.shape)
        infected_count = np.zeros(Y.shape)

        for person in self.people:
            px = (person.pos.x+self.hwidth)
            py = (person.pos.y+self.hheight)

            px = closest_mul(px, gran)
            py = closest_mul(py, gran)

            person_count[int(px), int(py)] += 1

            if infection_type is None:
                infected_count[int(px), int(py)] += len(person.infections)
            else:
                for infection in person.infections:
                    if isinstance(infection, infection_type):
                        infected_count[int(px), int(py)] += 1
                        break
        data = infected_count/person_count

        return X, Y, data

    def update_display(self):
        X, Y, data = self.get_heatmap_data(gran=self.gran)
        self.heatmap.set_array(data.ravel())
        #self.r_plot

    def run(self, update_num, interval=100, display=True, record=False):
        if display:
            anim = FuncAnimation(self.heatmap_fig, self.update, frames=update_num, interval=interval)
            if not record:
                plt.show()
        else:
            for i in range(update_num):
                self.update(i, display=False)

ORIGIN_VECTOR = Vector2D(x=0, y=0)

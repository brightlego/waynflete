import base
import person_hashmap
import numpy as np



class COVID(base.BaseInfection):
    RECOVER_TIME = 15
    RECOVER_STANDARD_DEV = 3.5
    INFECT_SUCCESS_CHANCE = 0.01
    DEIMUNISE_CHANCE = 0.02


class Model(base.BaseModel):
    VERSION = "1.0.4"
    def get_people_around(self, pos):
        people_around = []

        for x in np.arange(
            pos.x - self.NEIGHBOUR_RANGE,
            pos.x + self.NEIGHBOUR_RANGE * 2,
            self.NEIGHBOUR_RANGE,
        ):
            for y in np.arange(
                pos.y - self.NEIGHBOUR_RANGE,
                pos.y + self.NEIGHBOUR_RANGE * 2,
                self.NEIGHBOUR_RANGE,
            ):
                for person in self.people.get(base.Vector2D(x, y)):
                    if person.distance(pos) < self.NEIGHBOUR_RANGE:
                        people_around.append(person)

        return people_around

    def get_people_between(self, bl, tr):
        people_between = set()

        for person in self:
            if bl.x < person.pos.x < tr.x and bl.y < person.pos.y < tr.y:
                people_between.add(person)

        return people_between

    def infect_random_people(self, infection_type=COVID, p_num=1):
        for _ in range(p_num):
            person = self.get_random_person()
            person.infect_with(infection_type)
            # person.finalise_update()



def main():
    m = Model(400, hwidth=20, hheight=20, gran=1)
    m.infect_random_people()
    m.run(1000, record=False)


if __name__ == "__main__":
    main()

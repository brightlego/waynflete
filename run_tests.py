import model
import time
import numpy as np


def test(
    person_num=1000,
    hwidth=100,
    hheight=100,
    run_time=100,
    verbose=False,
    include_init=True,
):
    if include_init:
        start = time.time()
    if verbose:
        print("Initilising model")
    m = model.Model(person_num, hwidth=hwidth, hheight=hheight, display=False)

    if verbose:
        print("Infecting random person")
    m.infect_random_people(p_num=1)

    if not include_init:
        start = time.time()

    if verbose:
        print("Running model")
    m.run(run_time)

    end = time.time()
    return end - start


def small_test():
    return test(400, 50, 50, 100, verbose=True)


def vary_population(
    pmin=10,
    pmax=1000,
    pstep=1,
    hwidth=20,
    hheight=20,
    run_time=100,
    repeats=10,
    include_init=True,
):
    tmin = []
    tmax = []
    tavg = []
    for person_num in range(pmin, pmax + pstep, pstep):
        print(person_num)
        t = []
        for _ in range(repeats):
            t.append(
                test(
                    person_num=person_num,
                    hwidth=hwidth,
                    hheight=hheight,
                    run_time=run_time,
                    include_init=include_init,
                )
            )
        tmin.append(min(t))
        tmax.append(max(t))
        tavg.append(sum(t) / len(t))

    return tmin, tmax, tavg


def vary_density(
    person_num=400,
    dmin=0.1,
    dmax=10,
    dstep=0.1,
    run_time=100,
    repeats=10,
    include_init=True,
):
    tmin = []
    tmax = []
    tavg = []
    for density in np.arange(dmin, dmax + dstep, dstep):
        print(density)
        hheight = np.sqrt(person_num / density)
        hwidth = hheight
        t = []
        for _ in range(repeats):
            t.append(
                test(
                    person_num=person_num,
                    hwidth=hwidth,
                    hheight=hheight,
                    run_time=run_time,
                    include_init=include_init,
                )
            )
        tmin.append(min(t))
        tmax.append(max(t))
        tavg.append(sum(t) / len(t))

    return tmin, tmax, tavg


def vary_population_const_density(
    pmin=10,
    pmax=1000,
    pstep=1,
    density=0.2,
    run_time=100,
    repeats=10,
    include_init=True,
):
    tmin = []
    tmax = []
    tavg = []
    for person_num in range(pmin, pmax + pstep, pstep):
        print(person_num)
        hheight = np.sqrt(person_num / density)
        hwidth = hheight
        t = []
        for _ in range(repeats):
            t.append(
                test(
                    person_num=person_num,
                    hwidth=hwidth,
                    hheight=hheight,
                    run_time=run_time,
                    include_init=include_init,
                )
            )
        tmin.append(min(t))
        tmax.append(max(t))
        tavg.append(sum(t) / len(t))

    return tmin, tmax, tavg

import numpy as np
from collections import defaultdict


def make_driver_dict(nr_of_races, dtype=np.int32):
    return defaultdict(lambda: np.zeros(nr_of_races + 1, dtype=dtype))


def get_point_systems_dict(nr_of_races, r_with, r_wo, grid, quali):
    point_systems = [
        {
            "name": "F1 A/B Raceresults",
            "sprints": True,
            "dir": "withDNF_withSprint/formula1_extended/F1_A_B",
            "driver_dict": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "driver_dict_a": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "driver_dict_b": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "results": r_with,
        },
        {
            "name": "F1 A/B Raceresults",
            "sprints": False,
            "dir": "withDNF_woSprint/formula1_extended/F1_A_B",
            "driver_dict": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "driver_dict_a": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "driver_dict_b": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "results": r_with,
        },
        {
            "name": "F1 A/B Raceresults",
            "sprints": False,
            "dir": "woDNF_woSprint/formula1_extended/F1_A_B",
            "driver_dict": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "driver_dict_a": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "driver_dict_b": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "results": r_wo,
        },
        {
            "name": "F1 A/B Raceresults",
            "sprints": True,
            "dir": "woDNF_withSprint/formula1_extended/F1_A_B",
            "driver_dict": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "driver_dict_a": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "driver_dict_b": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "results": r_wo,
        },
        {
            "name": "F1 A/B Gridresults",
            "sprints": True,
            "dir": "withDNF_withSprint/formula1_extended/F1_A_B",
            "driver_dict": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "driver_dict_a": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "driver_dict_b": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "results": grid,
        },
        {
            "name": "F1 A/B Gridresults",
            "sprints": False,
            "dir": "withDNF_woSprint/formula1_extended/F1_A_B",
            "driver_dict": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "driver_dict_a": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "driver_dict_b": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "results": grid,
        },
        {
            "name": "F1 A/B Qualifyingresults",
            "sprints": False,
            "dir": "woDNF_woSprint/formula1_extended/F1_A_B",
            "driver_dict": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "driver_dict_a": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "driver_dict_b": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "results": quali,
        },
        {
            "name": "F1 A/B Qualifyingresults",
            "sprints": True,
            "dir": "woDNF_withSprint/formula1_extended/F1_A_B",
            "driver_dict": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "driver_dict_a": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "driver_dict_b": defaultdict(lambda: np.zeros(nr_of_races + 1)),
            "results": quali,
        },
    ]
    return point_systems

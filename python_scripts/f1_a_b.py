import numpy as np
from plot_help import plot_help
import f1_a_b_dict as psd

qualiresults = np.genfromtxt(
    "results/Qualifyingresults.txt", dtype=None, delimiter=",", autostrip=True
)
gridresults = np.genfromtxt(
    "results/Gridresults.txt", dtype=None, delimiter=",", autostrip=True
)
raceresults_with = np.genfromtxt(
    f"results/Raceresults_withDNF.txt", dtype=None, delimiter=",", autostrip=True
)
raceresults_wo = np.genfromtxt(
    f"results/Raceresults_woDNF.txt", dtype=None, delimiter=",", autostrip=True
)

with open("helpfiles/races.txt", "r") as f:
    races = f.read().splitlines()

driver_data = np.genfromtxt(
    "helpfiles/driver_data.txt",
    delimiter=",",
    dtype=[
        ("number", "i4"),
        ("shorthand", "U10"),
        ("name", "U50"),
        ("color", "U10"),
        ("style", "U10"),
        ("marker", "U10"),
    ],
    comments="#",
    names=True,
    autostrip=True,
)

f1_a = [
    "Verstappen",
    "Hadjar",
    "Norris",
    "Leclerc",
    "Sainz",
    "Russell",
    "Alonso",
    "Hülkenberg",
    "Ocon",
    "Gasly",
]
f1_b = [
    "Tsunoda",
    "Lawson",
    "Piastri",
    "Hamilton",
    "Albon",
    "Antonelli",
    "Stroll",
    "Bortoleto",
    "Bearman",
    "Colapinto",
    "Doohan",
]

race_points = np.array([25, 18, 15, 12, 10, 8, 6, 4, 2, 1], dtype=np.int32)
sprint_points = np.array([8, 7, 6, 5, 4, 3, 2, 1] + [0] * 2, dtype=np.int32)

nr_of_races = len(races)

point_systems = psd.get_point_systems_dict(
    len(races), raceresults_with, raceresults_wo, gridresults, qualiresults
)

for race_number, race in enumerate(races):
    is_sprint = "Sprint" in race
    for system in point_systems:
        if is_sprint and not system["sprints"]:
            for dn in system["driver_dict_a"].keys():
                system["driver_dict_a"][dn][race_number + 1] = system["driver_dict_a"][
                    dn
                ][race_number]
            for dn in system["driver_dict_b"].keys():
                system["driver_dict_b"][dn][race_number + 1] = system["driver_dict_b"][
                    dn
                ][race_number]
        else:
            result_a = []
            result_b = []
            for driver in system["results"][race_number][1:]:
                if driver in f1_a:
                    result_a.append(str(driver))
                elif driver in f1_b:
                    result_b.append(str(driver))
            for i, driver in enumerate(result_a):
                score_array = sprint_points if is_sprint else race_points
                system["driver_dict_a"][driver][race_number + 1] = (
                    system["driver_dict_a"][driver][race_number] + score_array[i]
                )
            for i, driver in enumerate(result_b):
                score_array = sprint_points if is_sprint else race_points
                system["driver_dict_b"][driver][race_number + 1] = (
                    system["driver_dict_b"][driver][race_number] + score_array[i]
                )

for system in point_systems:
    system["driver_dict"] = system["driver_dict_a"] | system["driver_dict_b"]

plot_help(point_systems, races, driver_data, f"_includes/")

print(f">>> f1_a_b.py done")

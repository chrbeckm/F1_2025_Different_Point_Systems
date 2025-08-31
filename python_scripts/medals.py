import os
import numpy as np
from collections import defaultdict

os.makedirs(f"_includes/medals", exist_ok=True)

qualiresults = np.genfromtxt(
    "results/Qualifyingresults.txt", dtype=None, delimiter=",", autostrip=True
)
gridresults = np.genfromtxt(
    "results/Gridresults.txt", dtype=None, delimiter=",", autostrip=True
)
raceresults = np.genfromtxt(
    "results/Raceresults_woDNF.txt", dtype=None, delimiter=",", autostrip=True
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
)["name"]

point_systems = [
    {
        "name": "F1 Medals Qualifyingresults",
        "driver_race": defaultdict(lambda: np.zeros(3)),
        "driver_sprint": defaultdict(lambda: np.zeros(3)),
    },
    {
        "name": "F1 Medals Gridresults",
        "driver_race": defaultdict(lambda: np.zeros(3)),
        "driver_sprint": defaultdict(lambda: np.zeros(3)),
    },
    {
        "name": "F1 Medals Raceresults",
        "driver_race": defaultdict(lambda: np.zeros(3)),
        "driver_sprint": defaultdict(lambda: np.zeros(3)),
    },
]

for race_number, race in enumerate(races):
    is_sprint = "Sprint" in race
    for system, current_result in zip(
        point_systems, [qualiresults, gridresults, raceresults]
    ):
        label = "driver_sprint" if is_sprint else "driver_race"
        for i in range(3):
            system[label][current_result[race_number][i + 1]][i] += 1

for system in point_systems:
    filename = f"_includes/medals/{system['name'].replace(' ', '_')}"
    with open(f"{filename}_races.csv", "w") as f:
        f.write("Races: Driver,Gold,Silber,Bronze\n")
        sorted_driver_race = sorted(
            (
                ("Undecided Events" if key == "" else key, value)
                for key, value in system["driver_race"].items()
            ),
            key=lambda item: (item[1][0], item[1][1], item[1][2]),
            reverse=True,
        )
        for dn, medals in sorted_driver_race:
            f.write(f"{dn},{int(medals[0])},{int(medals[1])},{int(medals[2])}\n")
    with open(f"{filename}_sprints.csv", "w") as f:
        f.write("Sprints: Driver,Gold,Silber,Bronze\n")
        sorted_driver_sprint = sorted(
            (
                ("Undecided Events" if key == "" else key, value)
                for key, value in system["driver_sprint"].items()
            ),
            key=lambda item: (item[1][0], item[1][1], item[1][2]),
            reverse=True,
        )
        for dn, medals in sorted_driver_sprint:
            f.write(f"{dn},{int(medals[0])},{int(medals[1])},{int(medals[2])}\n")

print(f">>> medals.py done")

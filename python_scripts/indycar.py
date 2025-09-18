import numpy as np
from collections import defaultdict
from plot_help import plot_help

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

with open("results/laps_led.txt", "r") as f:
    laps_lines = f.read().splitlines()
ll = [_.split(",")[::2] for _ in laps_lines[1:]]

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

points = np.array(
    [50, 40, 35, 32, 30, 28, 26, 24, 22, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10]
)
sprint_points = (points * 8) // 25
pole_position = 1
lead_most_laps = 2
lead_one_lap = 1
monaco_quali = np.array([_ for _ in range(12, 0, -1)] + [0] * 8)

nr_of_races = len(races)

point_systems = [
    {
        "name": "Indycar with Sprints and DNF",
        "sprints": True,
        "DNF": True,
        "dir": "withDNF/other_motorsport/Indycar",
        "driver_dict": defaultdict(lambda: np.zeros(nr_of_races + 1)),
        "r_results": raceresults_with,
        "q_results": gridresults,
    },
    {
        "name": "Indycar without Sprints and with DNF",
        "sprints": False,
        "DNF": True,
        "dir": "noSprints/withDNF/other_motorsport/Indycar",
        "driver_dict": defaultdict(lambda: np.zeros(nr_of_races + 1)),
        "r_results": raceresults_with,
        "q_results": gridresults,
    },
    {
        "name": "Indycar without Sprints and DNF",
        "sprints": False,
        "DNF": False,
        "dir": "noSprints/woDNF/other_motorsport/Indycar",
        "driver_dict": defaultdict(lambda: np.zeros(nr_of_races + 1)),
        "r_results": raceresults_wo,
        "q_results": qualiresults,
    },
    {
        "name": "Indycar with Sprints and without DNF",
        "sprints": True,
        "DNF": False,
        "dir": "woDNF/other_motorsport/Indycar",
        "driver_dict": defaultdict(lambda: np.zeros(nr_of_races + 1)),
        "r_results": raceresults_wo,
        "q_results": qualiresults,
    },
]

for race_number, race in enumerate(races):
    is_sprint = "Sprint" in race
    for system in point_systems:
        if not is_sprint or (is_sprint and system["sprints"]):
            for dn in driver_data["name"]:
                added_score = 0
                if dn in system["q_results"][race_number, :]:
                    # Pole and Qualifying
                    if "Monaco" in race:
                        pos_index = (
                            np.where(dn == system["q_results"][race_number, :])[0][0]
                            - 1
                        )
                        added_score += monaco_quali[pos_index]
                    elif dn == system["q_results"][race_number, 1]:
                        added_score += pole_position
                # Laps lead
                if dn in ll[race_number]:
                    if dn == ll[race_number][0]:
                        added_score += lead_most_laps
                    else:
                        added_score += lead_one_lap
                # Raceresult points
                if dn in system["r_results"][race_number, :]:
                    pos_index = (
                        np.where(dn == system["r_results"][race_number, :])[0][0] - 1
                    )
                    if is_sprint:
                        added_score += sprint_points[pos_index]
                    else:
                        added_score += points[pos_index]
                    system["driver_dict"][dn][race_number + 1] = (
                        system["driver_dict"][dn][race_number] + added_score
                    )
                else:
                    system["driver_dict"][dn][race_number + 1] = system["driver_dict"][
                        dn
                    ][race_number]

        else:
            for dn in driver_data["name"]:
                system["driver_dict"][dn][race_number + 1] = system["driver_dict"][dn][
                    race_number
                ]

plot_help(point_systems, races, driver_data)

print(f">>> indycar.py done")

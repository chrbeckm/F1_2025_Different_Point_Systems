import os
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from plot_help import plot_help, sorted_legend_by_final_points

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

with open("results/fastest_lap.txt", "r") as f:
    fl = f.read().splitlines()
fastest_lap = [_.split(",")[0] for _ in fl[1:]]

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

f125 = np.array([25, 18, 15, 12, 10, 8, 6, 4, 2, 1] + [0] * 10, dtype=np.int32)
f125_s = np.array([8, 7, 6, 5, 4, 3, 2, 1] + [0] * 12, dtype=np.int32)

# Multipliers
point_finish = 1.0
podium = 0.5  # resets
# Extra points
fastest_lap_points = 10.0
pole_position = 10.0
fastest_lap_points_sprints = int(fastest_lap_points * 8.0 / 25.0)
pole_position_sprints = int(pole_position * 8.0 / 25.0)

nr_of_races = len(races)

point_systems = [
    {
        "name": "Balatro with Sprints",
        "sprints": True,
        "dir": "withDNF/math/Balatro",
        "driver_dict": defaultdict(lambda: np.zeros(nr_of_races + 1)),
        "point_finishes": defaultdict(lambda: np.zeros(nr_of_races + 1)),
        "podium": defaultdict(lambda: np.zeros(nr_of_races + 1)),
        "r_results": raceresults_with,
        "q_results": gridresults,
    },
    {
        "name": "Balatro without Sprints",
        "sprints": False,
        "dir": "noSprints/withDNF/math/Balatro",
        "driver_dict": defaultdict(lambda: np.zeros(nr_of_races + 1)),
        "point_finishes": defaultdict(lambda: np.zeros(nr_of_races + 1)),
        "podium": defaultdict(lambda: np.zeros(nr_of_races + 1)),
        "r_results": raceresults_with,
        "q_results": gridresults,
    },
]

for system in point_systems:
    for race_number, race in enumerate(races):
        is_sprint = "Sprint" in race
        if not is_sprint or (is_sprint and system["sprints"]):
            for dn in driver_data["name"]:
                added_score = 0
                system["point_finishes"][dn][race_number + 1] = system[
                    "point_finishes"
                ][dn][race_number]
                if dn == system["q_results"][race_number, 1]:
                    added_score += pole_position_sprints if is_sprint else pole_position
                if dn == fastest_lap[race_number]:
                    added_score += (
                        fastest_lap_points_sprints if is_sprint else fastest_lap_points
                    )
                if dn in system["r_results"][race_number, :]:
                    pos_index = (
                        np.where(dn == system["r_results"][race_number, :])[0][0] - 1
                    )
                    if is_sprint:
                        added_score += f125_s[pos_index]
                    else:
                        added_score += f125[pos_index]
                    if pos_index < 10:
                        system["point_finishes"][dn][race_number + 1] += point_finish
                        if pos_index < 3:
                            system["podium"][dn][race_number + 1] += (
                                system["podium"][dn][race_number] + podium
                            )
                        else:
                            system["podium"][dn][race_number + 1] += 0
                    system["driver_dict"][dn][race_number + 1] = system["driver_dict"][
                        dn
                    ][race_number] + added_score * (
                        system["point_finishes"][dn][race_number]
                        + system["podium"][dn][race_number]
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
                system["point_finishes"][dn][race_number + 1] = system[
                    "point_finishes"
                ][dn][race_number]
                system["podium"][dn][race_number + 1] = system["podium"][dn][
                    race_number
                ]


# Plot
plot_help(point_systems, races, driver_data)

for j, system in enumerate(point_systems):
    x = np.arange(len(races) + 1)

    zero_arr = np.zeros((len(driver_data["name"]), len(races)))
    point_readout = [zero_arr] * len(point_systems)
    os.makedirs(system["dir"], exist_ok=True)
    fig, ax = plt.subplots(layout="constrained", figsize=(11.69, 8.27))
    for i, (di, dn) in enumerate(zip(driver_data["shorthand"], driver_data["name"])):
        data = system["podium"][dn] + system["point_finishes"][dn]
        ax.plot(
            x,
            data,
            label=f"{data[-1]:5.1f} {di}",
            color=f"#{driver_data['color'][i]}",
            linestyle=driver_data["style"][i],
        )
        point_readout[j][i] = np.diff(system["driver_dict"][dn])
    ax.set_title(f"{system['name']} - Multiplier")
    sorted_legend_by_final_points(ax)
    ax.grid()
    ax.set_xlim(0, 30)
    ax.set_ylim(0, ax.get_ylim()[-1])
    ax.set_xticks(
        np.arange(31),
        labels=[""] + races,
        rotation=-45,
        ha="left",
        rotation_mode="anchor",
    )

    filename = f"_includes/{system['dir']}/{system['name'].replace(' ', '_')}"
    # fig.savefig(filename + "_multiplier.pdf")
    fig.savefig(filename + "_multiplier.png", dpi=500)
    plt.close(fig)


print(f">>> balatro.py done")

import os
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

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
        "dir": "_includes/withDNF/other_motorsport/Indycar",
        "driver_dict": defaultdict(lambda: np.zeros(nr_of_races + 1)),
        "r_results": raceresults_with,
        "q_results": gridresults,
    },
    {
        "name": "Indycar without Sprints and with DNF",
        "sprints": False,
        "DNF": True,
        "dir": "_includes/noSprints/withDNF/other_motorsport/Indycar",
        "driver_dict": defaultdict(lambda: np.zeros(nr_of_races + 1)),
        "r_results": raceresults_with,
        "q_results": gridresults,
    },
    {
        "name": "Indycar without Sprints and DNF",
        "sprints": False,
        "DNF": False,
        "dir": "_includes/noSprints/woDNF/other_motorsport/Indycar",
        "driver_dict": defaultdict(lambda: np.zeros(nr_of_races + 1)),
        "r_results": raceresults_wo,
        "q_results": qualiresults,
    },
    {
        "name": "Indycar with Sprints and without DNF",
        "sprints": True,
        "DNF": False,
        "dir": "_includes/woDNF/other_motorsport/Indycar",
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


# Plot
def sorted_legend_by_final_points(ax):
    handles, labels = ax.get_legend_handles_labels()
    points_in_labels = [float(label.split()[0]) for label in labels]
    sorted_items = sorted(
        zip(handles, labels, points_in_labels), key=lambda item: item[2], reverse=True
    )
    sorted_handles, sorted_labels, _ = zip(*sorted_items)
    ax.legend(
        sorted_handles,
        sorted_labels,
        loc="center left",
        bbox_to_anchor=(1.0, 0.5),
    )


x = np.arange(len(races) + 1)

zero_arr = np.zeros((len(driver_data["name"]), len(races)))
point_readout = [zero_arr] * len(point_systems)
for j, system in enumerate(point_systems):
    os.makedirs(system["dir"], exist_ok=True)
    fig, ax = plt.subplots(layout="constrained", figsize=(11.69, 8.27))
    for i, (di, dn) in enumerate(zip(driver_data["shorthand"], driver_data["name"])):
        ax.plot(
            x,
            system["driver_dict"][dn],
            label=f"{system['driver_dict'][dn][-1]:5.0f} {di}",
            color=f"#{driver_data['color'][i]}",
            linestyle=driver_data["style"][i],
        )
        point_readout[j][i] = np.diff(system["driver_dict"][dn])
    ax.set_title(f"{system['name']}")
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

    filename = f"{system['dir']}/{system['name'].replace(' ', '_')}"
    fig.savefig(filename + ".pdf")
    fig.savefig(filename + ".png", dpi=500)
    plt.close(fig)
    np.savetxt(
        filename + ".csv",
        point_readout[j].T,
        header=", ".join(driver_data["name"]),
        fmt="%.d",
        delimiter=",",
    )

    RacingBulls = np.zeros(31)
    RedBull = np.zeros(31)
    for i, (tsu, law) in enumerate(
        zip(
            np.diff(system["driver_dict"]["Tsunoda"]),
            np.diff(system["driver_dict"]["Lawson"]),
        )
    ):
        if i < 3:
            RacingBulls[i + 1] = tsu + RacingBulls[i]
            RedBull[i + 1] = law + RedBull[i]
        else:
            RacingBulls[i + 1] = law + RacingBulls[i]
            RedBull[i + 1] = tsu + RedBull[i]
    team_dict = {
        "Alpine": system["driver_dict"]["Doohan"]
        + system["driver_dict"]["Gasly"]
        + system["driver_dict"]["Colapinto"],
        "AstonMartin": system["driver_dict"]["Alonso"]
        + system["driver_dict"]["Stroll"],
        "Ferrari": system["driver_dict"]["Leclerc"] + system["driver_dict"]["Hamilton"],
        "Haas": system["driver_dict"]["Ocon"] + system["driver_dict"]["Bearman"],
        "KickSauber": system["driver_dict"]["Bortoleto"]
        + system["driver_dict"]["Hülkenberg"],
        "McLaren": system["driver_dict"]["Norris"]
        + system["driver_dict"]["Verstappen"],
        "Mercedes": system["driver_dict"]["Antonelli"]
        + system["driver_dict"]["Russell"],
        "RacingBulls": system["driver_dict"]["Hadjar"] + RacingBulls,
        "RedBull": system["driver_dict"]["Verstappen"] + RedBull,
        "Williams": system["driver_dict"]["Albon"] + system["driver_dict"]["Sainz"],
    }
    fig, ax = plt.subplots(layout="constrained", figsize=(11.69, 8.27))
    ax.plot(
        x,
        team_dict["Alpine"],
        label=f"{team_dict['Alpine'][-1]:5.0f} Alpine",
        color="#0093cc",
        linestyle="solid",
    )
    ax.plot(
        x,
        team_dict["AstonMartin"],
        label=f"{team_dict['AstonMartin'][-1]:5.0f} Aston Martin",
        color="#229971",
        linestyle="solid",
    )
    ax.plot(
        x,
        team_dict["Ferrari"],
        label=f"{team_dict['Ferrari'][-1]:5.0f} Ferrari",
        color="#e80020",
        linestyle="solid",
    )
    ax.plot(
        x,
        team_dict["Haas"],
        label=f"{team_dict['Haas'][-1]:5.0f} Haas",
        color="#b6babd",
        linestyle="solid",
    )
    ax.plot(
        x,
        team_dict["KickSauber"],
        label=f"{team_dict['KickSauber'][-1]:5.0f} Kick Sauber",
        color="#52e252",
        linestyle="solid",
    )
    ax.plot(
        x,
        team_dict["McLaren"],
        label=f"{team_dict['McLaren'][-1]:5.0f} McLaren",
        color="#ff8000",
        linestyle="solid",
    )
    ax.plot(
        x,
        team_dict["Mercedes"],
        label=f"{team_dict['Mercedes'][-1]:5.0f} Mercedes",
        color="#27f4d2",
        linestyle="solid",
    )
    ax.plot(
        x,
        team_dict["RacingBulls"],
        label=f"{team_dict['RacingBulls'][-1]:5.0f} Racing Bulls",
        color="#6692ff",
        linestyle="solid",
    )
    ax.plot(
        x,
        team_dict["RedBull"],
        label=f"{team_dict['RedBull'][-1]:5.0f} Red Bull",
        color="#3671C6",
        linestyle="solid",
    )
    ax.plot(
        x,
        team_dict["Williams"],
        label=f"{team_dict['Williams'][-1]:5.0f} Williams",
        color="#64c4ff",
        linestyle="solid",
    )
    ax.set_title(f"{system['name']} Constructors' Championship")
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

    filename = f"{system['dir']}/constructors_{system['name'].replace(' ', '_')}"
    fig.savefig(filename + ".pdf")
    fig.savefig(filename + ".png", dpi=500)
    plt.close(fig)

print(f">>> indycar.py done")

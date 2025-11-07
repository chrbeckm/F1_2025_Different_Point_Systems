import numpy as np
import matplotlib.pyplot as plt
import os
from collections import defaultdict

qualiresults = np.genfromtxt(
    "results/Qualifyingresults.txt", dtype=None, delimiter=",", autostrip=True
)
gridresults = np.genfromtxt(
    "results/Gridresults.txt", dtype=None, delimiter=",", autostrip=True
)
raceresults_wo = np.genfromtxt(
    f"results/Raceresults_woDNF.txt", dtype=None, delimiter=",", autostrip=True
)
raceresults_with = np.genfromtxt(
    f"results/Raceresults_withDNF.txt", dtype=None, delimiter=",", autostrip=True
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

nr_of_races = len(races)

point_systems = [
    {
        "name": "Qualifyingresults",
        "driver_positions": defaultdict(lambda: np.full(nr_of_races, 21)),
        "driver_mean": defaultdict(lambda: np.full(nr_of_races, 21.0)),
        "results": qualiresults,
        "dir": "_includes/mean/qualifying",
    },
    {
        "name": "Gridpositions",
        "driver_positions": defaultdict(lambda: np.full(nr_of_races, 21)),
        "driver_mean": defaultdict(lambda: np.full(nr_of_races, 21.0)),
        "results": gridresults,
        "dir": "_includes/mean/grid",
    },
    {
        "name": "Raceresults without DNF",
        "driver_positions": defaultdict(lambda: np.full(nr_of_races, 21)),
        "driver_mean": defaultdict(lambda: np.full(nr_of_races, 21.0)),
        "results": raceresults_wo,
        "dir": "_includes/mean/raceresults_without_DNF",
    },
    {
        "name": "Raceresults with DNF",
        "driver_positions": defaultdict(lambda: np.full(nr_of_races, 21)),
        "driver_mean": defaultdict(lambda: np.full(nr_of_races, 21.0)),
        "results": raceresults_with,
        "dir": "_includes/mean/raceresults_with_DNF",
    },
]

x = np.arange(len(races))


def sorted_legend_by_final_points(ax, axtitle):
    handles, labels = ax.get_legend_handles_labels()
    points_in_labels = [float(label.split()[0]) for label in labels]
    sorted_items = sorted(
        zip(handles, labels, points_in_labels), key=lambda item: item[2], reverse=False
    )
    sorted_handles, sorted_labels, _ = zip(*sorted_items)
    ax.legend(
        sorted_handles,
        sorted_labels,
        loc="center left",
        bbox_to_anchor=(1.0, 0.5),
        title=axtitle,
    )


for system in point_systems:
    os.makedirs(system["dir"], exist_ok=True)
    for race_number, race in enumerate(races):
        for dn in driver_data["name"]:
            pos_index = np.where(system["results"][race_number, :] == dn)[0]
            if pos_index.size > 0:
                system["driver_positions"][dn][race_number] = pos_index[0]
            mask = system["driver_positions"][dn] < 21
            if np.sum(mask) != 0:
                system["driver_mean"][dn][race_number] = np.mean(
                    system["driver_positions"][dn][mask]
                )

    filename = f"{system['dir']}/positions"
    fig, ax = plt.subplots(layout="constrained", figsize=(11.69, 8.27))
    fig2d, ax2d = plt.subplots(layout="constrained", figsize=(11.69, 8.27))
    with open(f"{filename}.csv", "w", newline="") as csvfile:
        csvfile.write(f"Driver," + ",".join(races) + "\n")
        for i, dn in enumerate(driver_data["name"]):
            csvfile.write(
                f"{dn}," + ",".join(map(str, system["driver_positions"][dn])) + "\n"
            )
            ax.plot(
                x,
                system["driver_positions"][dn],
                label=f"{system['driver_positions'][dn].sum():d}  {driver_data['shorthand'][i]}",
                color=f"#{driver_data['color'][i]}",
                marker=driver_data["marker"][i],
                linestyle="",
            )
            ax.plot(
                x,
                system["driver_positions"][dn],
                color=f"#{driver_data['color'][i]}",
                alpha=0.2,
            )
        for i, dn in enumerate(driver_data["name"]):
            drivercolor = f"#{driver_data['color'][i]}"
            shorthand = driver_data["shorthand"][i]
            for race_idx, pos in enumerate(system["driver_positions"][dn]):
                # Only plot if position is valid
                if pos < 21:
                    # y = position, x = race index
                    rect = plt.Rectangle(
                        (race_idx - 0.5, pos - 0.5),
                        1,
                        1,
                        facecolor=drivercolor,
                        edgecolor="black",
                        linewidth=0.1,
                    )
                    ax2d.add_patch(rect)
                    ax2d.text(
                        race_idx,
                        pos,
                        shorthand,
                        ha="center",
                        va="center",
                        color=(
                            "black" if driver_data["style"][i] == "solid" else "white"
                        ),
                        fontsize=9,
                        fontweight="bold",
                    )
    ax.set_title(f"{system['name']} - Positions")
    sorted_legend_by_final_points(ax, "Sum of all Positions")
    ax.set_xlim(-0.5, 29.5)
    ax.set_ylim(0.5, 20.5)
    ax.set_xticks(x, labels=races, rotation=-45, ha="left", rotation_mode="anchor")
    ax.set_yticks(np.arange(1, 21))
    ax.yaxis.set_inverted(True)
    fig.savefig(f"{filename}.png", dpi=500)
    # fig.savefig(f"{filename}.pdf")
    plt.close(fig)

    ax2d.set_title(f"{system['name']} - Positions")
    ax2d.set_xlim(-0.5, len(races) - 0.5)
    ax2d.set_ylim(0.5, 20.5)
    ax2d.set_xticks(x, labels=races, rotation=-45, ha="left", rotation_mode="anchor")
    ax2d.set_yticks(np.arange(1, 21))
    ax2d.yaxis.set_inverted(True)
    fig2d.savefig(f"{filename}_2D.png")
    # fig2d.savefig(f"{filename}_2D.pdf")
    plt.close(fig2d)

    filename = f"{system['dir']}/mean"
    fig, ax = plt.subplots(layout="constrained", figsize=(11.69, 8.27))
    with open(f"{filename}.csv", "w", newline="") as csvfile:
        csvfile.write(f"Driver," + ",".join(races) + "\n")
        for i, dn in enumerate(driver_data["name"]):
            csvfile.write(
                f"{dn},"
                + ",".join([f"{x:.2f}" for x in system["driver_mean"][dn]])
                + "\n"
            )
            ax.plot(
                x,
                system["driver_mean"][dn],
                label=f"{system['driver_mean'][dn][-1]:6.2f} {driver_data['shorthand'][i]}",
                color=f"#{driver_data['color'][i]}",
                linestyle=driver_data["style"][i],
            )
    ax.set_title(f"{system['name']} - Mean Positions")
    sorted_legend_by_final_points(ax, "Final Mean Positions")
    ax.set_xlim(-0.5, 29.5)
    ax.set_ylim(0.5, 20.5)
    ax.set_xticks(x, labels=races, rotation=-45, ha="left", rotation_mode="anchor")
    ax.set_yticks(np.arange(1, 21))
    ax.yaxis.set_inverted(True)
    fig.savefig(f"{filename}.png")
    # fig.savefig(f"{filename}.pdf")
    plt.close(fig)

team_max_dict = {
    "Alpine,Doohan,Gasly,Colapinto": 0,
    "AstonMartin,Alonso,Stroll": 0,
    "Ferrari,Leclerc,Hamilton": 0,
    "Haas,Ocon,Bearman": 0,
    "KickSauber,Bortoleto,Hülkenberg": 0,
    "McLaren,Norris,Piastri": 0,
    "Mercedes,Antonelli,Russell": 0,
    "RacingBulls,Hadjar,Lawson": 0,
    "RedBull,Tsunoda,Verstappen": 0,
    "Williams,Albon,Sainz": 0,
}

for i, dn in enumerate(driver_data["name"]):
    for system in point_systems:
        counts = np.bincount(system["driver_positions"][dn])[1:-1]
        print(dn, np.max(counts))
        for key in team_max_dict.keys():
            if dn in key and np.max(counts) > team_max_dict[key]:
                team_max_dict[key] = np.max(counts)

for k in team_max_dict.keys():
    print(k, team_max_dict[k], sep="\t")

dp_dir = "_includes/mean/driver_positions/"
os.makedirs(dp_dir, exist_ok=True)
for i, (dn, dc) in enumerate(zip(driver_data["name"], driver_data["color"])):
    fig, ax = plt.subplots(
        4, layout="constrained", figsize=(11.69, 8.27), sharex=True, sharey=True
    )
    group_data = [
        (point_systems[0], "Qualifying times"),
        (point_systems[1], "Grid positions"),
        (point_systems[2], "Race results without DNF"),
        (point_systems[3], "Race results with DNF"),
    ]
    for p, (system, label_text) in enumerate(group_data):
        counts = np.bincount(system["driver_positions"][dn])
        bar_positions = np.arange(len(counts))
        ax[p].bar(
            bar_positions,
            counts,
            width=0.8,
            color=f"#{dc}",
            label=label_text,
            align="center",
            zorder=2,
        )
        upper_ylim = 0
        for key in team_max_dict.keys():
            if dn in key and upper_ylim < team_max_dict[key]:
                upper_ylim = team_max_dict[key]
        print(dn, upper_ylim)
        ax[p].set_xlim(0.5, 20.5)
        ax[p].set_ylim(0, upper_ylim + 0.5)
        ax[p].set_xticks(np.arange(1, 21))
        ax[p].set_yticks(np.arange(upper_ylim + 1))
        ax[p].legend(loc="upper right")
        ax[p].grid(axis="y", zorder=1)
    fig.suptitle(f"Positions for {dn}")
    fig.savefig(f"{dp_dir}{dn}.png", dpi=500)
    plt.close(fig)

print(f">>> mean_positions.py done")

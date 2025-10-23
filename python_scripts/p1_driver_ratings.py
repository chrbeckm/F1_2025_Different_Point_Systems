import os
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
from plot_help import plot_help, sorted_legend_by_final_points


def cummean_ignore_nan(x):
    x = np.array(x, dtype=float)
    valid = ~np.isnan(x)
    csum = np.nancumsum(x)
    counts = np.cumsum(valid)
    return np.divide(csum, counts, out=np.full_like(csum, np.nan), where=counts > 0)


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

ratings = np.genfromtxt(
    "results/p1_driver_ratings.txt",
    delimiter=",",
    autostrip=True,
    unpack=True,
    dtype=["U50"] * 3 + ["f4"] * 21,
    encoding="utf-8",
)

with open("results/p1_driver_ratings.txt", "r") as f:
    driver_order = f.read().splitlines()[0].split(",")[3:]

races = ratings[0][1::3]
nr_of_races = len(races)

p1_matt = ratings[2][0::3]
p1_tommy = ratings[2][1::3]

pure_ratings = ratings[3:]

point_systems = [
    {
        "name": "Matt",
        "dir": "p1_wMT/",
        "driver_dict": defaultdict(lambda: np.zeros(nr_of_races + 1)),
        "ratings_mean": defaultdict(lambda: np.zeros(nr_of_races)),
    },
    {
        "name": "Tommy",
        "dir": "p1_wMT/",
        "driver_dict": defaultdict(lambda: np.zeros(nr_of_races + 1)),
        "ratings_mean": defaultdict(lambda: np.zeros(nr_of_races)),
    },
    {
        "name": "Audience",
        "dir": "p1_wMT/",
        "driver_dict": defaultdict(lambda: np.zeros(nr_of_races + 1)),
        "ratings_mean": defaultdict(lambda: np.zeros(nr_of_races)),
    },
]

for p, system in enumerate(point_systems):
    for i, d in enumerate(driver_order):
        system["driver_dict"][d][1:] = np.nancumsum(pure_ratings[i][p::3]).astype(int)
        system["ratings_mean"][d] = cummean_ignore_nan(pure_ratings[i][p::3])

plot_help(point_systems, races.tolist(), driver_data, "_includes")


def sorted_legend_by_final_points(ax, axtitle):
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
        title=axtitle,
    )


x = np.arange(nr_of_races)

for system in point_systems:
    filename = f"_includes/{system['dir']}/{system["name"]}_average"
    fig, ax = plt.subplots(layout="constrained", figsize=(11.69, 8.27))
    for i, dn in enumerate(driver_data["name"]):
        ax.plot(
            x,
            system["ratings_mean"][dn],
            label=f"{system['ratings_mean'][dn][-1]:6.2f}  {driver_data['shorthand'][i]}",
            color=f"#{driver_data['color'][i]}",
            linestyle=driver_data["style"][i],
        )
    ax.set_title(f"{system['name']}'s Driver Ratings - Rolling Average")
    sorted_legend_by_final_points(ax, "Average")
    ax.set_xlim(-0.5, x[-1] + 0.5)
    ax.set_ylim(0.5, 10.5)
    ax.set_xticks(x, labels=races, rotation=-45, ha="left", rotation_mode="anchor")
    fig.savefig(f"{filename}.png", dpi=500)
    plt.close(fig)

for list, file in zip([p1_matt, p1_tommy], ["matt", "tommy"]):
    no_empty_strings = [_ for _ in list if _]
    counts = Counter(no_empty_strings)
    sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    with open(f"_includes/p1_wMT/{file}_p1.csv", "w") as f:
        f.write("Driver,Number of P1 awards\n")
        for name, count in sorted_counts:
            f.write(f"{name},{count}\n")

print(f">>> p1_driver_ratings.py done")

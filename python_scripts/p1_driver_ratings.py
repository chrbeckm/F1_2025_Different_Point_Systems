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

pure_ratings = np.array(ratings[3:])

point_systems = [
    {
        "id": "Matt",
        "name": "Matt - Sum of ratings",
        "dir": "p1_wMT/Matt/",
        "driver_dict": defaultdict(lambda: np.zeros(nr_of_races + 1)),
        "ratings_mean": defaultdict(lambda: np.zeros(nr_of_races)),
        "race_mean": np.zeros(nr_of_races),
    },
    {
        "id": "Tommy",
        "name": "Tommy - Sum of ratings",
        "dir": "p1_wMT/Tommy/",
        "driver_dict": defaultdict(lambda: np.zeros(nr_of_races + 1)),
        "ratings_mean": defaultdict(lambda: np.zeros(nr_of_races)),
        "race_mean": np.zeros(nr_of_races),
    },
    {
        "id": "Audience",
        "name": "Audience - Sum of ratings",
        "dir": "p1_wMT/Audience",
        "driver_dict": defaultdict(lambda: np.zeros(nr_of_races + 1)),
        "ratings_mean": defaultdict(lambda: np.zeros(nr_of_races)),
        "race_mean": np.zeros(nr_of_races),
    },
]

for p, system in enumerate(point_systems):
    for i, d in enumerate(driver_order):
        system["driver_dict"][d][1:] = np.nancumsum(pure_ratings[i][p::3]).astype(int)
        system["ratings_mean"][d] = cummean_ignore_nan(pure_ratings[i][p::3])
    for i, r in enumerate(races):
        if np.count_nonzero(np.isnan(pure_ratings.T[p + i * 3])) < 20:
            system["race_mean"][i] = np.nanmean(pure_ratings.T[p + i * 3])

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
    filename = f"_includes/{system['dir']}/{system['id']}_average"
    fig, ax = plt.subplots(layout="constrained", figsize=(11.69, 8.27))
    for i, dn in enumerate(driver_data["name"]):
        ax.plot(
            x,
            system["ratings_mean"][dn],
            label=f"{system['ratings_mean'][dn][-1]:6.2f}  {driver_data['shorthand'][i]}",
            color=f"#{driver_data['color'][i]}",
            linestyle=driver_data["style"][i],
        )
    ax.set_title(f"{system['id']}'s Driver Ratings - Rolling Average")
    sorted_legend_by_final_points(ax, "Average")
    ax.set_xlim(-0.5, x[-1] + 0.5)
    ax.set_ylim(0.5, 10.5)
    ax.set_xticks(x, labels=races, rotation=-45, ha="left", rotation_mode="anchor")
    fig.savefig(f"{filename}.png", dpi=500)
    plt.close(fig)


for list, file in zip([p1_matt, p1_tommy], ["Matt", "Tommy"]):
    no_empty_strings = [_ for _ in list if _]
    counts = Counter(no_empty_strings)
    sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    with open(f"_includes/p1_wMT/{file}/{file}_p1.csv", "w") as f:
        f.write("Driver,Number of P1 awards\n")
        for name, count in sorted_counts:
            f.write(f"{name},{count}\n")

fig, ax = plt.subplots(layout="constrained", figsize=(11.69, 8.27))
ax.plot(x, point_systems[0]["race_mean"], color="#e80020", label="Matt")
ax.plot(x, point_systems[1]["race_mean"], color="#3671C6", label="Tommy")
ax.plot(x, point_systems[2]["race_mean"], color="black", label="Audience")
ax.set_title(f"Average Driver Ratings in Race")
ax.set_xlim(0, x[-1])
ax.set_ylim(5.5, 7.5)
ax.grid()
ax.legend()
ax.set_xticks(x, labels=races, rotation=-45, ha="left", rotation_mode="anchor")
fig.savefig(f"_includes/p1_wMT/race_averages.png", dpi=500)
plt.close(fig)

# Find max for team
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

for i, dn in enumerate(driver_order):
    for p in range(3):
        y = pure_ratings[i][p::3][~np.isnan(pure_ratings[i][p::3])].astype(int)
        counts = np.bincount(y)
        for key in team_max_dict.keys():
            if dn in key and np.max(counts) > team_max_dict[key]:
                team_max_dict[key] = np.max(counts)

os.makedirs("_includes/p1_wMT/driver_ratings/", exist_ok=True)
for i, dn in enumerate(driver_order):
    fig, ax = plt.subplots(
        3, layout="constrained", figsize=(11.69, 8.27), sharex=True, sharey=True
    )
    group_data = [
        ("Matt", "#e80020"),
        ("Tommy", "#3671C6"),
        ("Audience", "black"),
    ]
    for p, (name, col) in enumerate(group_data):
        y = pure_ratings[i][p::3][~np.isnan(pure_ratings[i][p::3])].astype(int)
        counts = np.bincount(y)
        bar_positions = np.arange(len(counts))
        ax[p].bar(
            bar_positions,
            counts,
            width=0.8,
            color=col,
            label=name,
            align="center",
            zorder=2,
        )
        upper_ylim = 0
        for key in team_max_dict.keys():
            if dn in key and upper_ylim < team_max_dict[key]:
                upper_ylim = team_max_dict[key]
        ax[p].set_xlim(-0.5, 10.5)
        ax[p].set_ylim(0, upper_ylim + 0.5)
        ax[p].set_xticks(np.arange(11))
        ax[p].set_yticks(np.arange(upper_ylim + 1))
        ax[p].legend(loc="upper left")
        ax[p].grid(axis="y", zorder=1)
    fig.suptitle(f"Ratings for {dn}")
    fig.savefig(f"_includes/p1_wMT/driver_ratings/{dn}.png", dpi=500)
    plt.close(fig)

for i, system in enumerate(point_systems):
    fig, ax = plt.subplots(layout="constrained", figsize=(11.69, 8.27))
    im = ax.imshow(pure_ratings[:, i::3], vmin=0, vmax=11, aspect="auto", cmap="hot")
    fig.colorbar(im, ax=ax)
    for d in range(pure_ratings[:, i::3].shape[0]):
        for r in range(pure_ratings[:, i::3].shape[1]):
            if np.isnan(pure_ratings[:, i::3][d, r]):
                text = ax.text(r, d, "~", ha="center", va="center", color="#3671C6")
            else:
                text = ax.text(
                    r,
                    d,
                    f"{pure_ratings[:, i::3][d, r]:.0f}",
                    ha="center",
                    va="center",
                    color="#3671C6",
                )
    ax.set_xticks(x, labels=races, rotation=-45, ha="left", rotation_mode="anchor")
    ax.set_yticks(np.arange(len(driver_order)), driver_order)
    fig.suptitle(f"Ratings from {system['id']}")
    fig.savefig(f"_includes/{system['dir']}/{system['id']}_2D.png", dpi=500)
    plt.close(fig)


print(f">>> p1_driver_ratings.py done")

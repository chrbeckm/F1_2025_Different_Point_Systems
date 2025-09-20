import os, csv
import numpy as np
import matplotlib.pyplot as plt


def sorted_legend_by_final_points(ax, bbox=(1.0, 0.5)):
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
        bbox_to_anchor=bbox,
    )


def plot_help(point_systems, races, driver_data, path="_includes"):
    for j, system in enumerate(point_systems):
        label_format = "{:7.1f} {}" if "Balatro" in system["name"] else "{:5.0f} {}"
        x = np.arange(len(races) + 1)

        zero_arr = np.zeros((len(driver_data["name"]), len(races)))
        point_readout = [zero_arr] * len(point_systems)
        os.makedirs(path + "/" + system["dir"], exist_ok=True)
        fig, ax = plt.subplots(layout="constrained", figsize=(11.69, 8.27))

        for i, (di, dn) in enumerate(
            zip(driver_data["shorthand"], driver_data["name"])
        ):
            ax.plot(
                x,
                system["driver_dict"][dn],
                label=label_format.format(system["driver_dict"][dn][-1], di),
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

        filename = f"{path}/{system['dir']}/{system['name'].replace(' ', '_')}"
        # fig.savefig(filename + ".pdf")
        fig.savefig(filename + ".png", dpi=500)
        plt.close(fig)
        data_with_race_names = []
        for race_idx, race in enumerate(races):
            row = [race] + list(point_readout[j][:, race_idx])
            data_with_race_names.append(row)

        full_points = np.zeros(driver_data.shape[0])
        for i, dn in enumerate(driver_data["name"]):
            full_points[i] = system["driver_dict"][dn][-1]

        with open(f"{filename}.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Race"] + driver_data["name"].tolist())
            writer.writerows(data_with_race_names)
            writer.writerow(["Σ"] + [f"{fp}" for fp in full_points])

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
            "Ferrari": system["driver_dict"]["Leclerc"]
            + system["driver_dict"]["Hamilton"],
            "Haas": system["driver_dict"]["Ocon"] + system["driver_dict"]["Bearman"],
            "KickSauber": system["driver_dict"]["Bortoleto"]
            + system["driver_dict"]["Hülkenberg"],
            "McLaren": system["driver_dict"]["Norris"]
            + system["driver_dict"]["Piastri"],
            "Mercedes": system["driver_dict"]["Antonelli"]
            + system["driver_dict"]["Russell"],
            "RacingBulls": system["driver_dict"]["Hadjar"] + RacingBulls,
            "RedBull": system["driver_dict"]["Verstappen"] + RedBull,
            "Williams": system["driver_dict"]["Albon"] + system["driver_dict"]["Sainz"],
        }
        fig, ax = plt.subplots(layout="constrained", figsize=(11.69, 8.27))
        teams = {
            "Alpine": ["#0093cc", "Alpine"],
            "AstonMartin": ["#229971", "Aston Martin"],
            "Ferrari": ["#e80020", "Ferrari"],
            "Haas": ["#b6babd", "Haas"],
            "KickSauber": ["#52e252", "Kick Sauber"],
            "McLaren": ["#ff8000", "McLaren"],
            "Mercedes": ["#27f4d2", "Mercedes"],
            "RacingBulls": ["#6692ff", "Racing Bulls"],
            "RedBull": ["#3671C6", "Red Bull"],
            "Williams": ["#64c4ff", "Williams"],
        }

        for team, (color, label) in teams.items():
            ax.plot(
                x,
                team_dict[team],
                label=label_format.format(team_dict[team][-1], label),
                color=color,
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

        filename = (
            f"{path}/{system['dir']}/constructors_{system['name'].replace(' ', '_')}"
        )
        # fig.savefig(filename + ".pdf")
        fig.savefig(filename + ".png", dpi=500)
        plt.close(fig)

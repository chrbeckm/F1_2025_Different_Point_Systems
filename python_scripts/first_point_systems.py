import os, sys
import numpy as np
import matplotlib.pyplot as plt
import first_point_systems_dict as psd
from plot_help import plot_help, sorted_legend_by_final_points

DNFdiff = sys.argv[1]
while DNFdiff not in ["withDNF", "woDNF"]:
    print("Choose with or without DNF.")
    DNFdiff = input("'withDNF' | 'woDNF':")

SprintDiff = sys.argv[2]
while SprintDiff not in ["withSprint", "woSprint"]:
    print("Choose with or without Sprints.")
    SprintDiff = input("'withSprint' | 'woSprint':")

# Ensure build directory exists
os.makedirs(f"_includes/{DNFdiff}", exist_ok=True)

if DNFdiff == "woDNF":
    qualiresults = np.genfromtxt(
        "results/Qualifyingresults.txt", dtype=None, delimiter=",", autostrip=True
    )
elif DNFdiff == "withDNF":
    qualiresults = np.genfromtxt(
        "results/Gridresults.txt", dtype=None, delimiter=",", autostrip=True
    )

raceresults = np.genfromtxt(
    f"results/Raceresults_{DNFdiff}.txt", dtype=None, delimiter=",", autostrip=True
)
with open("results/fastest_lap.txt", "r") as f:
    fl = f.read().splitlines()
fastest_lap = [_.split(",")[0] for _ in fl[1:]]

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

point_systems = psd.get_point_systems_dict(len(races))

# Process race results
for race_number, race in enumerate(races):
    is_sprint = "Sprint" in race
    if not (is_sprint and SprintDiff == "woSprint"):
        for system in point_systems:
            # Load results, if the dict is for quali results, or other results
            results = qualiresults if system.get("qualifying") else raceresults
            current_result = results[race_number, 1:]
            finishers = np.count_nonzero(current_result)
            # Check which point system to use
            if not system.get("is_drivernumbers"):
                if system.get("scrabble") and "2025" not in system["name"]:
                    score_array = (
                        [
                            int(_ * system["scale"])
                            for _ in system["points"][race_number]
                        ]
                        if is_sprint
                        else system["points"][race_number]
                    )
                elif system.get("scrabble") and "2025" in system["name"]:
                    score_array = (
                        system["sprint_points"][race_number]
                        if is_sprint
                        else system["points"][race_number]
                    )
                elif system.get("scale"):
                    score_array = (
                        [int(_ * system["scale"]) for _ in system["points"]]
                        if is_sprint
                        else system["points"]
                    )
                else:
                    score_array = (
                        system["sprint_points"] if is_sprint else system["points"]
                    )
            for dn in driver_data["name"]:
                prev_score = system["driver_dict"][dn][race_number]
                if dn in current_result:
                    pos_index = np.where(dn == current_result)[0][0]
                    if system.get("is_drivernumbers"):
                        numbers_in_race = np.zeros(20)
                        i = 0
                        for dname in driver_data["name"]:
                            if dname in current_result:
                                numbers_in_race[i] = driver_data["number"][
                                    driver_data["name"] == dname
                                ][0]
                                i += 1
                        numbers_in_race = np.sort(numbers_in_race, kind="mergesort")[
                            ::-1
                        ]
                        raw_points = numbers_in_race[pos_index]
                        score = (
                            int(raw_points * system["scale"])
                            if is_sprint
                            else raw_points
                        )
                    elif "reversed" in system["name"]:
                        score = score_array[finishers - pos_index - 1]
                    else:
                        score = score_array[pos_index]
                    if (system.get("fastest_lap") == True and not is_sprint) or (
                        system.get("sprint_fastest_lap") == True and is_sprint
                    ):
                        score_array = (
                            system["sprint_fastest_lap"]
                            if is_sprint
                            else system["fastest_lap"]
                        )
                        score += score_array(
                            np.where(dn == fastest_lap[race_number])[0][0]
                        )

                    system["driver_dict"][dn][race_number + 1] = prev_score + score
                else:
                    system["driver_dict"][dn][race_number + 1] = prev_score


imsa, imsa_q, f150, f150q, f188, f188q, f125, mksc, mkscq = 0, 0, 0, 0, 0, 0, 0, 0, 0
for i in range(len(point_systems)):
    if point_systems[i]["name"] == "IMSA":
        imsa = i
    elif point_systems[i]["name"] == "IMSA q":
        imsa_q = i
    elif point_systems[i]["name"] == "F1 1950 Raceresults":
        f150 = i
    elif point_systems[i]["name"] == "F1 1950 Qualifyingresults":
        f150q = i
    elif point_systems[i]["name"] == "F1 1988 Raceresults":
        f188 = i
    elif point_systems[i]["name"] == "F1 1988 Qualifyingresults":
        f188q = i
    elif point_systems[i]["name"] == "F1 2025 Raceresults":
        f125 = i
    elif point_systems[i]["name"] == "Super Mario Kart Raceresults":
        mksc = i
    elif point_systems[i]["name"] == "Super Mario Kart Qualifyingresults":
        mkscq = i

print("Now combining IMSA points, check for names:")
print(f"{point_systems[imsa]['name']} & {point_systems[imsa_q]['name']}")
for dn in driver_data["name"]:
    point_systems[imsa]["driver_dict"][dn] += point_systems[imsa_q]["driver_dict"][dn]

x = np.arange(len(races) + 1)


if DNFdiff == "withDNF" and SprintDiff == "withSprint":
    os.makedirs(f"_includes/{DNFdiff}/{point_systems[f125]['dir']}", exist_ok=True)
    fig, ax = plt.subplots(layout="constrained", figsize=(11.69, 8.27))
    for i, (di, dn) in enumerate(zip(driver_data["shorthand"], driver_data["name"])):
        ax.plot(
            x,
            point_systems[f125]["driver_dict"][dn],
            label=f"{point_systems[f125]['driver_dict'][dn][-1]:5.0f} {di}",
            color=f"#{driver_data['color'][i]}",
            linestyle=driver_data["style"][i],
        )
    ax.set_title(
        f"{point_systems[f125]['name']} {DNFdiff[:-3].replace('wo', 'without')} DNF"
    )
    sorted_legend_by_final_points(ax, (-0.14, 0.5))
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
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()

    filename = f"_includes/{DNFdiff}/{point_systems[f125]['dir']}/{point_systems[f125]['name'].replace(' ', '_')}_leftLegend"
    # fig.savefig(filename + ".pdf")
    fig.savefig(filename + ".png", dpi=500)
    plt.close(fig)
    print("F1 2025 plot done", DNFdiff)

plot_help(point_systems, races, driver_data, f"_includes/{DNFdiff}_{SprintDiff}")

# F1 1950: only 4 best results count
# F1 1988: only 11 best results count
for system_nr in [f150, f150q, f188, f188q]:
    system = point_systems[system_nr]
    sum_index = 4 if "50" in system["name"] else 11

    # collect driver names and summed points
    driver_names = driver_data["name"]
    points = []
    for dn in driver_names:
        score = np.sum(np.sort(np.diff(system["driver_dict"][dn]))[::-1][:sum_index])
        points.append(score)

    # sort drivers by points descending
    sorted_indices = np.argsort(points)[::-1]
    sorted_names = driver_names[sorted_indices]
    sorted_points = np.array(points)[sorted_indices]

    filename = f"_includes/{DNFdiff}/{system['dir']}/{system['name'].replace(' ', '_')}"
    with open(f"{filename}_summedPoints.csv", "w") as f:
        # first row: drivers
        f.write(",".join(sorted_names) + "\n")
        # second row: points
        f.write(",".join(map(str, sorted_points)) + "\n")


print(f">>> {sys.argv} done")

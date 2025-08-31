import os
import numpy as np

os.makedirs(f"_includes/eel", exist_ok=True)

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

eel_quali = np.genfromtxt(
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
eel_grid = np.genfromtxt(
    "helpfiles/driver_data.txt",
    delimiter=",",
    dtype=[
        ("number", "i4"),
        ("shorthand", "U10"),
        ("name", "U50"),
        ("color", "U10"),
        ("style", "U10"),
    ],
    comments="#",
    names=True,
    autostrip=True,
)["name"]
eel_races = np.genfromtxt(
    "helpfiles/driver_data.txt",
    delimiter=",",
    dtype=[
        ("number", "i4"),
        ("shorthand", "U10"),
        ("name", "U50"),
        ("color", "U10"),
        ("style", "U10"),
    ],
    comments="#",
    names=True,
    autostrip=True,
)["name"]
eliminated_quali = []
eliminated_grid = []
eliminated_race = []
last_race = 0

for race_number, race in enumerate(races):
    if not "Sprint" in race:
        for eliminated, driver_list, results in zip(
            [eliminated_quali, eliminated_grid, eliminated_race],
            [eel_quali, eel_grid, eel_races],
            [qualiresults, gridresults, raceresults],
        ):
            current_result = results[race_number, 1:]
            for i in range(1, 21):
                if current_result[-i] in driver_list:
                    driver_list[np.where(driver_list == current_result[-i])[0]] = 0
                    eliminated.append(current_result[-i])
                    last_race = race_number
                    break
print(last_race)

with open("_includes/eel/Qualifying.csv", "w") as fq:
    fq.write(
        f"Race:, {', '.join([_ for _ in races if 'Sprint' not in _])},Still Driving\n"
    )
    fq.write(
        f"Eliminated Driver:, {', '.join([_ for _ in eliminated_quali])}{','*(27-last_race)}{'; '.join([_[:] for _ in np.sort(eel_quali) if _ != '0'])}\n"
    )

with open("_includes/eel/Grid.csv", "w") as fq:
    fq.write(
        f"Race:, {', '.join([_ for _ in races if 'Sprint' not in _])},Still Driving\n"
    )
    fq.write(
        f"Eliminated Driver:, {', '.join([_ for _ in eliminated_grid])}{','*(27-last_race)}{'; '.join([_[:] for _ in np.sort(eel_grid) if _ != '0'])}\n"
    )

with open("_includes/eel/Races.csv", "w") as fq:
    fq.write(
        f"Race:, {', '.join([_ for _ in races if 'Sprint' not in _])},Still Driving\n"
    )
    fq.write(
        f"Eliminated Driver:, {', '.join([_ for _ in eliminated_race])}{','*(27-last_race)}{'; '.join([_[:] for _ in np.sort(eel_races) if _ != '0'])}\n"
    )

print(f">>> eel.py done")

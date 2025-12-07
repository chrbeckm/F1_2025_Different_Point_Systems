import first_point_systems_dict as psd
import os

os.makedirs("_includes/points/", exist_ok=True)

point_systems = psd.get_point_systems_dict(1)

for system in point_systems:
    if not system.get("qualifying"):
        if not system.get("is_drivernumbers", False):
            if "crabble" not in system["name"]:
                filename = (
                    "_includes/points/"
                    + system["name"].replace(" Raceresults", "").replace(" ", "_").replace("ğ", "g")
                    + ".md"
                )
                with open(filename, "w") as file:
                    file.write("| Event / Position | ")
                    file.write(" | ".join(map(str, [_ for _ in range(1, 21)])))
                    file.write(f" |\n|{' - |' * 21}\n| Sprint | ")
                    file.write(" | ".join(map(str, system["sprint_points"])))
                    file.write(" |\n| Race | ")
                    file.write(f"{' | '.join(map(str, system['points']))} |")

print(f">>> print_points.py done")

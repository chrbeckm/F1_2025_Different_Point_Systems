import numpy as np
from collections import defaultdict


def make_driver_dict(nr_of_races, dtype=np.int32):
    return defaultdict(lambda: np.zeros(nr_of_races + 1, dtype=dtype))


def get_point_systems_dict(nr_of_races):
    # Scoring systems
    f125 = np.array([25, 18, 15, 12, 10, 8, 6, 4, 2, 1] + [0] * 10, dtype=np.int32)
    f125_s = np.array([8, 7, 6, 5, 4, 3, 2, 1] + [0] * 12, dtype=np.int32)
    f125_11 = np.array([0] * 10 + [25, 18, 15, 12, 10, 8, 6, 4, 2, 1], dtype=np.int32)
    f125_11_s = np.array([0] * 10 + [8, 7, 6, 5, 4, 3, 2, 1, 0, 0], dtype=np.int32)
    f121_s = np.array([3, 2, 1] + [0] * 17, dtype=np.int32)
    inverse_position = np.arange(20, 0, -1, dtype=np.int32)
    f125_proposal = np.array(
        [25, 18, 15, 12, 10, 8, 6, 5, 4, 3, 2, 1] + [0] * 8, dtype=np.int32
    )
    f150 = np.array([8, 6, 4, 3, 2] + [0] * 15, dtype=np.int32)  # 4 best
    f181 = np.array([9, 6, 4, 3, 2, 1] + [0] * 14, dtype=np.int32)  # 11 best
    f191 = np.array([10, 6, 4, 3, 2, 1] + [0] * 14, dtype=np.int32)
    f2_s = np.array([10, 8, 6, 5, 4, 3, 2, 1] + [0] * 12, dtype=np.int32)
    imsa = np.array(
        [
            35,
            32,
            30,
            28,
            26,
            25,
            24,
            23,
            22,
            21,
            20,
            19,
            18,
            17,
            16,
            15,
            14,
            13,
            12,
            11,
        ],
        dtype=np.int32,
    )
    f103 = np.array([10, 8, 6, 5, 4, 3, 2, 1] + [0] * 12, dtype=np.int32)
    motoGP = np.array(
        [25, 20, 16, 13, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1] + [0] * 5, dtype=np.int32
    )
    motoGP_s = np.array([12, 9, 7, 6, 5, 4, 3, 2, 1] + [0] * 11, dtype=np.int32)
    mariokart_sc = np.array([3, 2, 1] + [0] * 17, dtype=np.int32)
    mariokart_ds = np.array([10, 8, 6, 4, 3, 2, 1] + [0] * 13, dtype=np.int32)
    mariokart_wii = np.array(
        [15, 12, 10, 8, 7, 6, 5, 4, 3, 2, 1] + [0] * 9, dtype=np.int32
    )
    mariokart_7 = np.array([10, 8, 6, 5, 4, 3, 2, 1] + [0] * 12, dtype=np.int32)
    mariokart_8 = np.array(
        [15, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1] + [0] * 8, dtype=np.int32
    )
    mariokart_world = np.array(
        [15, 12, 10, 9, 9, 8, 8, 7, 7, 6, 6, 6, 5, 5, 5, 4, 4, 4, 3, 3], dtype=np.int32
    )
    scrabble = np.genfromtxt("helpfiles/scrabble.txt")

    fibonacci = np.array(
        [
            4181,
            2584,
            1597,
            987,
            610,
            377,
            233,
            144,
            89,
            55,
            34,
            21,
            13,
            8,
            5,
            3,
            2,
            1,
            1,
            0,
        ],
        dtype=np.int32,
    )
    primes = np.array(
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71],
        dtype=np.int32,
    )
    tommo = np.array(
        [40, 34, 30, 26, 23, 20, 18, 16, 14, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        dtype=np.int32,
    )
    tommo_s = np.array(
        [16, 14, 12, 10, 8, 7, 6, 5, 4, 3, 2, 1] + [0] * 8,
        dtype=np.int32,
    )
    esc = np.array([12, 10, 8, 7, 6, 5, 4, 3, 2, 1] + [0] * 10, dtype=np.int32)

    empty_1P = np.array([1] + [0] * 19, dtype=np.int32)

    point_systems = [
        {
            "name": "F1 2025 Raceresults",
            "points": f125,
            "sprint_points": f125_s,
            "driver_dict": make_driver_dict(nr_of_races),
            "dir": "formula1/2025",
        },
        {
            "name": "F1 2025 Qualifyingresults",
            "points": f125,
            "sprint_points": f125_s,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "dir": "formula1/2025",
        },
        {
            "name": "F1 2025 Points from 11th Raceresults",
            "points": f125_11,
            "sprint_points": f125_11_s,
            "driver_dict": make_driver_dict(nr_of_races),
            "dir": "formula1_extended/2025_11th",
        },
        {
            "name": "F1 2025 Points from 11th Qualifyingresults",
            "points": f125_11,
            "sprint_points": f125_11_s,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "dir": "formula1_extended/2025_11th",
        },
        {
            "name": "Inverse Position Raceresults",
            "points": inverse_position,
            "sprint_points": (inverse_position * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "dir": "formula1_extended/Inverse",
        },
        {
            "name": "Inverse Position Qualifyingresults",
            "points": inverse_position,
            "sprint_points": (inverse_position * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "dir": "formula1_extended/Inverse",
        },
        {
            "name": "Drivernumbers Raceresults",
            "scale": 8 / 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "is_drivernumbers": True,
            "dir": "drivernumbers",
        },
        {
            "name": "Drivernumbers Qualifyingresults",
            "scale": 8 / 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "is_drivernumbers": True,
            "qualifying": True,
            "dir": "drivernumbers",
        },
        {
            "name": "F1 2022 - 2024 Raceresults",
            "points": f125,
            "sprint_points": f125_s,
            "driver_dict": make_driver_dict(nr_of_races),
            "fastest_lap": empty_1P,
            "fl_until": 10,
            "dir": "formula1/2022",
        },
        {
            "name": "F1 2021 Raceresults",
            "points": f125,
            "sprint_points": f121_s,
            "driver_dict": make_driver_dict(nr_of_races),
            "fastest_lap": empty_1P,
            "fl_until": 10,
            "fl_sprint_until": 8,
            "dir": "formula1/2021",
        },
        {
            "name": "F1 2021 Qualifyingresults",
            "points": f125,
            "sprint_points": f121_s,
            "driver_dict": make_driver_dict(nr_of_races),
            "fastest_lap": empty_1P,
            "fl_until": 10,
            "fl_sprint_until": 8,
            "qualifying": True,
            "dir": "formula1/2021",
        },
        {
            "name": "F1 2025 Proposal Raceresults",
            "points": f125_proposal,
            "sprint_points": f125_s,
            "driver_dict": make_driver_dict(nr_of_races),
            "fastest_lap": empty_1P,
            "dir": "formula1_extended/2025_proposal",
        },
        {
            "name": "F1 2025 Proposal Qualifyingresults",
            "points": f125_proposal,
            "sprint_points": f125_s,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "fastest_lap": empty_1P,
            "dir": "formula1_extended/2025_proposal",
        },
        {
            "name": "F2 2025 Raceresults",
            "points": f125,
            "sprint_points": f2_s,
            "driver_dict": make_driver_dict(nr_of_races),
            "pole_points": empty_1P * 2,
            "fastest_lap": empty_1P,
            "sprint_fastest_lap": empty_1P,
            "fl_until": 10,
            "fl_sprint_until": 10,
            "dir": "other_motorsport/F2",
        },
        {
            "name": "Formula E Raceresults",
            "points": f125,
            "sprint_points": (f125 * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            # "fastest_lap": empty_1P,
            "pole_points": empty_1P * 3,
            "dir": "other_motorsport/FE",
        },
        {
            "name": "IMSA",
            "points": imsa * 10,
            "sprint_points": (imsa * 80) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "dir": "other_motorsport/IMSA",
        },
        {
            "name": "IMSA q",
            "points": imsa,
            "sprint_points": (imsa * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "dir": "other_motorsport/IMSA",
        },
        {
            "name": "IMSA",
            "points": imsa * 10,
            "sprint_points": (imsa * 80) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "dir": "other_motorsport/IMSA",
        },
        {
            "name": "IMSA q",
            "points": imsa,
            "sprint_points": (imsa * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "dir": "other_motorsport/IMSA",
        },
        {
            "name": "F1 1991 - 2002 Raceresults",
            "points": f191,
            "sprint_points": (f191 * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "dir": "formula1/1991",
        },
        {
            "name": "F1 1991 - 2002 Qualifyingresults",
            "points": f191,
            "sprint_points": (f191 * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "dir": "formula1/1991",
        },
        {
            "name": "F1 2003 - 2009 Raceresults",
            "points": f103,
            "sprint_points": (f103 * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "dir": "formula1/2003",
        },
        {
            "name": "F1 2003 - 2009 Qualifyingresults",
            "points": f103,
            "sprint_points": (f103 * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "dir": "formula1/2003",
        },
        {
            "name": "Mariokart DS Raceresults",
            "points": mariokart_ds,
            "sprint_points": (mariokart_ds * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "dir": "mariokart/DS",
        },
        {
            "name": "Mariokart DS Qualifyingresults",
            "points": mariokart_ds,
            "sprint_points": (mariokart_ds * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "dir": "mariokart/DS",
        },
        {
            "name": "Mariokart Wii Raceresults",
            "points": mariokart_wii,
            "sprint_points": (mariokart_wii * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "dir": "mariokart/Wii",
        },
        {
            "name": "Mariokart Wii Qualifyingresults",
            "points": mariokart_wii,
            "sprint_points": (mariokart_wii * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "dir": "mariokart/Wii",
        },
        {
            "name": "Mariokart 7 Raceresults",
            "points": mariokart_7,
            "sprint_points": (mariokart_7 * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "dir": "mariokart/7",
        },
        {
            "name": "Mariokart 7 Qualifyingresults",
            "points": mariokart_7,
            "sprint_points": (mariokart_7 * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "dir": "mariokart/7",
        },
        {
            "name": "Mariokart 8 Raceresults",
            "points": mariokart_8,
            "sprint_points": (mariokart_8 * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "dir": "mariokart/8",
        },
        {
            "name": "Mariokart 8 Qualifyingresults",
            "points": mariokart_8,
            "sprint_points": (mariokart_8 * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "dir": "mariokart/8",
        },
        {
            "name": "Mariokart World Raceresults",
            "points": mariokart_world,
            "sprint_points": (mariokart_world * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "dir": "mariokart/world",
        },
        {
            "name": "Mariokart World Qualifyingresults",
            "points": mariokart_world,
            "sprint_points": (mariokart_world * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "dir": "mariokart/world",
        },
        {
            "name": "Scrabble Raceresults",
            "points": scrabble,
            "scale": 8 / 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "scrabble": True,
            "dir": "games/scrabble",
        },
        {
            "name": "Scrabble Qualifyingresults",
            "points": scrabble,
            "scale": 8 / 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "scrabble": True,
            "dir": "games/scrabble",
        },
        {
            "name": "Scrabble + F1 2025 Raceresults",
            "points": scrabble + f125,
            "sprint_points": scrabble + f125_s,
            "driver_dict": make_driver_dict(nr_of_races),
            "scrabble": True,
            "dir": "games/scrabble/PlusF12025",
        },
        {
            "name": "Scrabble + F1 2025 Qualifyingresults",
            "points": scrabble + f125,
            "sprint_points": scrabble + f125_s,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "scrabble": True,
            "dir": "games/scrabble/PlusF12025",
        },
        {
            "name": "F1 2025 Reversed Raceresults",
            "points": f125,
            "sprint_points": f125_s,
            "driver_dict": make_driver_dict(nr_of_races),
            "dir": "formula1_extended/2025_reversed",
        },
        {
            "name": "F1 2025 Reversed Qualifyingresults",
            "points": f125,
            "sprint_points": f125_s,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "dir": "formula1_extended/2025_reversed",
        },
        {
            "name": "F1 1950 - 1953 Raceresults",
            "points": f150,
            "sprint_points": (f150 * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "driver_sum": defaultdict(lambda: 0),
            "fastest_lap": empty_1P,
            "dir": "formula1/1950",
        },
        {
            "name": "F1 1950 - 1953 Qualifyingresults",
            "points": f150,
            "sprint_points": (f150 * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "driver_sum": defaultdict(lambda: 0),
            "qualifying": True,
            "fastest_lap": empty_1P,
            "dir": "formula1/1950",
        },
        {
            "name": "F1 1981 - 1990 Raceresults",
            "points": f181,
            "sprint_points": (f181 * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "driver_sum": defaultdict(lambda: 0),
            "dir": "formula1/1981",
        },
        {
            "name": "F1 1981 - 1990 Qualifyingresults",
            "points": f181,
            "sprint_points": (f181 * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "driver_sum": defaultdict(lambda: 0),
            "qualifying": True,
            "dir": "formula1/1981",
        },
        {
            "name": "Super Mario Kart Raceresults",
            "points": mariokart_sc,
            "sprint_points": (mariokart_sc * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "dir": "mariokart/SMK",
        },
        {
            "name": "Super Mario Kart Qualifyingresults",
            "points": mariokart_sc,
            "sprint_points": (mariokart_sc * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "dir": "mariokart/SMK",
        },
        {
            "name": "Fibonacci Raceresults",
            "points": fibonacci,
            "sprint_points": (fibonacci * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "dir": "math/fibonacci",
        },
        {
            "name": "Fibonacci Qualifyingresults",
            "points": fibonacci,
            "sprint_points": (fibonacci * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "dir": "math/fibonacci",
        },
        {
            "name": "Prime Numbers Raceresults",
            "points": primes[::-1],
            "sprint_points": (primes[::-1] * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "dir": "math/prime",
        },
        {
            "name": "Prime Numbers Qualifyingresults",
            "points": primes[::-1],
            "sprint_points": (primes[::-1] * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "dir": "math/prime",
        },
        {
            "name": "Squared Numbers Raceresults",
            "points": inverse_position**2,
            "sprint_points": inverse_position,
            "driver_dict": make_driver_dict(nr_of_races),
            "dir": "math/squared",
        },
        {
            "name": "Squared Numbers Qualifyingresults",
            "points": inverse_position**2,
            "sprint_points": inverse_position,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "dir": "math/squared",
        },
        {
            "name": "Tommo (yt) Raceresults",
            "points": tommo,
            "sprint_points": tommo_s,
            "driver_dict": make_driver_dict(nr_of_races),
            "dir": "yt/tommo",
        },
        {
            "name": "Tommo (yt) Qualifyingresults",
            "points": tommo,
            "sprint_points": tommo_s,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "dir": "yt/tommo",
        },
        {
            "name": "Moto GP Raceresults",
            "points": motoGP,
            "sprint_points": motoGP_s,
            "driver_dict": make_driver_dict(nr_of_races),
            "dir": "other_motorsport/motoGP",
        },
        {
            "name": "Moto GP Qualifyingresults",
            "points": motoGP,
            "sprint_points": motoGP_s,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "dir": "other_motorsport/motoGP",
        },
        {
            "name": "DTM Raceresults",
            "points": motoGP,
            "sprint_points": (motoGP * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "pole_points": f121_s,
            "dir": "other_motorsport/DTM",
        },
        {
            "name": "DTM Qualifyingresults",
            "points": motoGP,
            "sprint_points": (motoGP * 8) // 25,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "pole_points": f121_s,
            "dir": "other_motorsport/DTM",
        },
        {
            "name": "Eurovision Song Contest Raceresults",
            "points": esc,
            "sprint_points": np.zeros(20, np.int32),
            "fastest_lap": esc,
            "driver_dict": make_driver_dict(nr_of_races),
            "dir": "other/ESC",
        },
        {
            "name": "Eurovision Song Contest Qualifyingresults",
            "points": esc,
            "sprint_points": np.zeros(20, np.int32),
            "fastest_lap": esc,
            "driver_dict": make_driver_dict(nr_of_races),
            "qualifying": True,
            "dir": "other/ESC",
        },
    ]
    return point_systems

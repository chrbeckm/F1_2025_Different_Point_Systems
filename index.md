---
layout: default
permalink: /
title: F1 2025 in different Point Systems
---

| Position based systems | Math | Formula 1 | Formula 1 related | Other Motorsport | Mariokart | Scrabble | Youtubers |
| - | - | - | - | - | - | - | - |
| [Positions](/F1_2025_Different_Point_Systems/positions) | [Prime Numbers](/F1_2025_Different_Point_Systems/prime) | [1950](/F1_2025_Different_Point_Systems/1950) | [F1 Medals](/F1_2025_Different_Point_Systems/F1Medals) | [IMSA](/F1_2025_Different_Point_Systems/imsa) | [Mariokart DS](/F1_2025_Different_Point_Systems/mariokart_DS) | [only Scrabble](/F1_2025_Different_Point_Systems/scrabble) | [Tommo](/F1_2025_Different_Point_Systems/tommo) |
| [Inverse Positions](/F1_2025_Different_Point_Systems/inverse_positions) | [Fibonacci](/F1_2025_Different_Point_Systems/fibonacci) | [1988](/F1_2025_Different_Point_Systems/1988) | [F1 2025 Proposal](/F1_2025_Different_Point_Systems/2025_proposal) | [Indycar](/F1_2025_Different_Point_Systems/indycar) | [Mariokart Wii](/F1_2025_Different_Point_Systems/mariokart_Wii) | [Scrabble + F1 2025](/F1_2025_Different_Point_Systems/scrabble_plus_f1_2025) | |
| [Mean Positions](/F1_2025_Different_Point_Systems/mean) | [Squared Numbers](/F1_2025_Different_Point_Systems/squared) | [2007](/F1_2025_Different_Point_Systems/2007) | [F1 2025 Reversed](/F1_2025_Different_Point_Systems/2025_reversed) | | [Mariokart 7](/F1_2025_Different_Point_Systems/mariokart_7) | | |
| [Everyone Except Last](/F1_2025_Different_Point_Systems/eel) | | [2021](/F1_2025_Different_Point_Systems/2021) | [F2](/F1_2025_Different_Point_Systems/F2_2025) | | [Mariokart 8](/F1_2025_Different_Point_Systems/mariokart_8) | | |
| | | [2024](/F1_2025_Different_Point_Systems/2024) | [Drivernumbers](/F1_2025_Different_Point_Systems/drivernumbers) | | [Mariokart World](/F1_2025_Different_Point_Systems/mariokart_World) | | |
| | | [2025](/F1_2025_Different_Point_Systems/2025) | | | | | |

Download all files in a zip [here](/F1_2025_Different_Point_Systems/docs/assets/all_files.zip).

[Comparison between all point systems and the Formula 1 2025 point system.](/F1_2025_Different_Point_Systems/overview)

# F1 2025 in different Point Systems - Explanation

We really enjoyed the videos from Mr. V on different point systems for F1 seasons,
so we wanted to try ourselfs on similar ones for the current season and our own ideas.

- [F1 2021 in alternative point systems](https://www.youtube.com/watch?v=5u08c8_WxSk)
- [F1 2007 in alternative point systems](https://www.youtube.com/watch?v=Gc2kF24cgXI)

More videos about this topic:
- [Tommo](https://www.youtube.com/watch?v=Da2TCf3K8JM)

For some systems we used the same points list for the sprints and the full races,
as those systems don't have sprint points. In those cases we used
```
int(points * 8 / 25)
```
to scale down the points.
8 / 25, because this is the scale difference between the official F1 points
and the transformation into integers, as we do not want weird floating points.

As we heard quite some time at the start of the season that it might be a
qualifying-based championship, we included, if possible,
a standing based on qualifying positions as well.

If multiple drivers have the same number of points,
there isn't a distinction implemented to differentiate between achieved positions.

Possible abbreviations are:
- woDNF: without DNF, results are then ordered based on lap retired,
  includes then the Qualifyingresults, purely based on the set times
- withDNF: with DNF, DSQ, DNS, etc. Then Gridpositions are used,
  so starting place penalties are taken into account.
- noSprints: As most other point systems don't have sprint points,
  there is the analysis, ignoring all sprint races

## Data taken from
  - <https://en.wikipedia.org/wiki/2025_Formula_One_World_Championship#Grands_Prix>
  - <https://www.statsf1.com/en/2025/hongrie/meilleur-tour.aspx>
  - Fastest Lap in Sprints: Race review on Sky F1 youtube channel

### Contact

Have suggestion for a new point system?

Found a bug?

[E-Mail](mailto:fdifferentpointsystem at gmail.com)

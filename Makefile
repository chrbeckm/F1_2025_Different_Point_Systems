TARGETSCRABBLE = helpfiles/scrabble.txt
TARGETEEL = _includes/eel/Grid.csv
TARGETBALATRO = _includes/withDNF/math/Balatro/Balatro_with_Sprints.pdf
TARGETMEAN = _includes/mean/grid/mean.csv
TARGETMEDALS = _includes/medals/F1_Medals_Gridresults_races.csv
TARGETINDYCAR = _includes/withDNF/other_motorsport/Indycar/Indycar_with_Sprints_and_DNF.png
TARGETwithDNF = _includes/withDNF/drivernumbers/constructors_Drivernumbers_Qualifyingresults.png
TARGETwoDNF = _includes/woDNF/drivernumbers/constructors_Drivernumbers_Qualifyingresults.png
TARGETnoSprintswithDNF = _includes/noSprints/withDNF/drivernumbers/constructors_Drivernumbers_Qualifyingresults.png
TARGETnoSprintswoDNF = _includes/noSprints/woDNF/drivernumbers/constructors_Drivernumbers_Qualifyingresults.png

HELPPLOT = python_scripts/plot_help.py
HELPDICT = python_scripts/first_point_systems_dict.py
HELPDRIVERDATA = helpfiles/driver_data.txt
HELPRACES = helpfiles/races.txt
RESULTFASTEST = results/fastest_lap.txt
RESULTLAPSLED = results/laps_led.txt
RESULTGRID = results/Gridresults.txt
RESULTQUALIFYING = results/Qualifyingresults.txt
RESULTwoDNF = results/Raceresults_woDNF.txt
RESULTwithDNF = results/Raceresults_withDNF.txt

all: _includes/eel/Grid.md \
	docs/assets/mean/qualifying/positions_2D.png

_includes/eel/Grid.md: \
	$(TARGETwithDNF) \
	$(TARGETwoDNF) \
	$(TARGETnoSprintswithDNF) \
	$(TARGETnoSprintswoDNF) \
	$(TARGETSCRABBLE) \
	$(TARGETEEL) \
	$(TARGETMEAN) \
	$(TARGETMEDALS) \
	$(TARGETINDYCAR) \
	$(TARGETBALATRO)
	find _includes -type f -name '*.csv' -exec sh -c 'for f; do csv2md "$$f" > "$${f%.csv}.md"; done' _ {} +

docs/assets/mean/qualifying/positions_2D.png: \
	$(TARGETwithDNF) \
	$(TARGETwoDNF) \
	$(TARGETnoSprintswithDNF) \
	$(TARGETnoSprintswoDNF) \
	$(TARGETMEAN) \
	$(TARGETMEDALS) \
	$(TARGETINDYCAR) \
	$(TARGETBALATRO)
	mkdir -p docs/assets
	find _includes -type f -name '*.png' \
	  -exec sh -c 'for f; do \
	    rel=$${f#_includes/}; \
	    mkdir -p "docs/assets/$$(dirname "$$rel")"; \
	    cp "$$f" "docs/assets/$$rel"; \
	  done' _ {} +
	zip -r all_files.zip _includes/eel _includes/mean _includes/medals _includes/noSprints _includes/withDNF _includes/woDNF
	mv all_files.zip docs/assets/

$(TARGETSCRABBLE): helpfiles/scrabble.py
	python $<

$(TARGETEEL): \
	python_scripts/eel.py \
	$(RESULTQUALIFYING) \
	$(RESULTGRID) \
	$(RESULTwoDNF) \
	$(HELPRACES) \
	$(HELPDRIVERDATA)
	python $<

$(TARGETBALATRO): \
	python_scripts/balatro.py \
	$(RESULTQUALIFYING) \
	$(RESULTwithDNF) \
	$(RESULTFASTEST) \
	$(HELPRACES) \
	$(HELPDRIVERDATA) \
	$(HELPPLOT)
	python $<

$(TARGETMEAN): \
	python_scripts/mean_positions.py \
	$(RESULTQUALIFYING) \
	$(RESULTGRID) \
	$(RESULTwoDNF) \
	$(RESULTwithDNF) \
	$(HELPRACES) \
	$(HELPDRIVERDATA)
	python $<

$(TARGETMEDALS): \
	python_scripts/medals.py \
	$(RESULTQUALIFYING) \
	$(RESULTGRID) \
	$(RESULTwoDNF) \
	$(HELPRACES) \
	$(HELPDRIVERDATA)
	python $<

$(TARGETINDYCAR): \
	python_scripts/indycar.py \
	$(RESULTQUALIFYING) \
	$(RESULTGRID) \
	$(RESULTwoDNF) \
	$(RESULTwithDNF) \
	$(RESULTLAPSLED) \
	$(HELPRACES) \
	$(HELPDRIVERDATA) \
	$(HELPPLOT)
	python $<

$(TARGETwithDNF): \
	python_scripts/first_point_systems.py \
	$(HELPDICT) \
	$(RESULTGRID) \
	$(RESULTwithDNF) \
	$(RESULTFASTEST) \
	$(HELPRACES) \
	$(HELPDRIVERDATA) \
	$(HELPPLOT)
	python $< with

$(TARGETwoDNF): \
	python_scripts/first_point_systems.py \
	$(HELPDICT) \
	$(RESULTQUALIFYING) \
	$(wDNF) \
	$(RESULTFASTEST) \
	$(HELPRACES) \
	$(HELPDRIVERDATA) \
	$(HELPPLOT)
	python $< wo

$(TARGETnoSprintswithDNF): \
	python_scripts/first_point_systems_noSprints.py \
	$(HELPDICT) \
	$(RESULTGRID) \
	$(RESULTwithDNF) \
	$(RESULTFASTEST) \
	$(HELPRACES) \
	$(HELPDRIVERDATA) \
	$(HELPPLOT)
	python $< with

$(TARGETnoSprintswoDNF): \
	python_scripts/first_point_systems_noSprints.py \
	$(HELPDICT) \
	$(RESULTQUALIFYING) \
	$(wDNF) \
	$(RESULTFASTEST) \
	$(HELPRACES) \
	$(HELPDRIVERDATA) \
	$(HELPPLOT)
	python $< wo

clean:
	rm -rf _includes
	rm -rf docs

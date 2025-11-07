TARGETSCRABBLE = helpfiles/scrabble.txt
TARGETEEL = _includes/eel/Grid.csv
TARGETBALATRO = _includes/withDNF_withSprint/math/Balatro/Balatro_with_Sprints.png
TARGETMEAN = _includes/mean/grid/mean.csv
TARGETMEDALS = _includes/medals/F1_Medals_Gridresults_races.csv
TARGETINDYCAR = _includes/withDNF_withSprint/other_motorsport/Indycar/Indycar_with_Sprints_and_DNF.png
TARGETF1AB = _includes/withDNF_withSprint/formula1_extended/F1_A_B/F1_A_Gridresults.png
TARGETP1wMT = _includes/p1_wMT/Matt/Matt_-_Sum_of_ratings.png
TARGETwithDNF = _includes/withDNF_withSprint/drivernumbers/constructors_Drivernumbers_Qualifyingresults.png
TARGETwoDNF = _includes/woDNF_withSprint/drivernumbers/constructors_Drivernumbers_Qualifyingresults.png
TARGETnoSprintswithDNF = _includes/withDNF_woSprint/drivernumbers/constructors_Drivernumbers_Qualifyingresults.png
TARGETnoSprintswoDNF = _includes/woDNF_woSprint/drivernumbers/constructors_Drivernumbers_Qualifyingresults.png

HELPPLOT = python_scripts/plot_help.py
HELPDICT = python_scripts/first_point_systems_dict.py
HELPABDICT = python_scripts/f1_a_b_dict.py
HELPDRIVERDATA = helpfiles/driver_data.txt
HELPRACES = helpfiles/races.txt
RESULTFASTEST = results/fastest_lap.txt
RESULTLAPSLED = results/laps_led.txt
RESULTGRID = results/Gridresults.txt
RESULTQUALIFYING = results/Qualifyingresults.txt
RESULTwoDNF = results/Raceresults_woDNF.txt
RESULTwithDNF = results/Raceresults_withDNF.txt
RESULTP1wMT = results/p1_driver_ratings.txt

all: _includes/eel/Grid.md \
	docs/assets/mean/qualifying/positions_2D.png \
	_includes/points/F1_1950.md

_includes/points/F1_1950.md: python_scripts/print_points.py	$(HELPDICT)
	python $<

pre_csv2md = $(TARGETwithDNF) $(TARGETwoDNF) $(TARGETnoSprintswithDNF) $(TARGETnoSprintswoDNF) \
	$(TARGETP1wMT) $(TARGETF1AB) $(TARGETSCRABBLE) $(TARGETEEL) $(TARGETMEAN) $(TARGETMEDALS) $(TARGETINDYCAR) $(TARGETBALATRO)
_includes/eel/Grid.md: $(pre_csv2md)
	find _includes -type f -name '*.csv' -exec sh -c 'for f; do csv2md "$$f" > "$${f%.csv}.md"; done' _ {} +

pre_docs = $(TARGETwithDNF) $(TARGETwoDNF) $(TARGETnoSprintswithDNF) $(TARGETnoSprintswoDNF) \
	$(TARGETP1wMT) $(TARGETF1AB) $(TARGETMEAN) $(TARGETMEDALS) $(TARGETINDYCAR) $(TARGETBALATRO)
docs/assets/mean/qualifying/positions_2D.png: $(pre_docs)
	mkdir -p docs/assets
	find _includes -type f -name '*.png' \
	  -exec sh -c 'for f; do \
	    rel=$${f#_includes/}; \
	    mkdir -p "docs/assets/$$(dirname "$$rel")"; \
	    cp "$$f" "docs/assets/$$rel"; \
	  done' _ {} +
	zip -r all_files.zip _includes/eel _includes/mean _includes/medals _includes/p1_wMT _includes/withDNF_withSprint _includes/withDNF_woSprint _includes/woDNF_withSprint _includes/woDNF_woSprint -x \*.md
	mv all_files.zip docs/assets/

$(TARGETSCRABBLE): helpfiles/scrabble.py
	python $<

pre_eel = $(RESULTQUALIFYING) $(RESULTGRID) $(RESULTwoDNF) $(HELPRACES) $(HELPDRIVERDATA)
$(TARGETEEL): python_scripts/eel.py $(pre_eel)
	python $<

pre_balatro = $(RESULTQUALIFYING) $(RESULTwithDNF) $(RESULTFASTEST) $(HELPRACES) $(HELPDRIVERDATA) $(HELPPLOT)
$(TARGETBALATRO): python_scripts/balatro.py $(pre_balatro)
	python $<

pre_mean = $(RESULTQUALIFYING) $(RESULTGRID) $(RESULTwoDNF) $(RESULTwithDNF) $(HELPRACES) $(HELPDRIVERDATA)
$(TARGETMEAN): python_scripts/mean_positions.py $(pre_mean)
	python $<

pre_medals = $(RESULTQUALIFYING) $(RESULTGRID) $(RESULTwoDNF) $(HELPRACES) $(HELPDRIVERDATA)
$(TARGETMEDALS): python_scripts/medals.py $(pre_medals)
	python $<

pre_indy = $(RESULTQUALIFYING) $(RESULTGRID) $(RESULTwoDNF) $(RESULTwithDNF) $(RESULTLAPSLED) $(HELPRACES) $(HELPDRIVERDATA) $(HELPPLOT)
$(TARGETINDYCAR): python_scripts/indycar.py $(pre_indy)
	python $<

pre_F1AB = $(RESULTQUALIFYING) $(RESULTGRID) $(RESULTwoDNF) $(RESULTwithDNF) $(HELPABDICT) $(HELPRACES) $(HELPDRIVERDATA) $(HELPPLOT)
$(TARGETF1AB): python_scripts/f1_a_b.py $(pre_F1AB)
	python $<

pre_wMT = $(RESULTP1wMT) $(HELPDRIVERDATA)
$(TARGETP1wMT): python_scripts/p1_driver_ratings.py $(pre_wMT)
	python $<

pre_with = $(HELPDICT) $(RESULTGRID) $(RESULTwithDNF) $(RESULTFASTEST) $(HELPRACES) $(HELPDRIVERDATA) $(HELPPLOT)
$(TARGETwithDNF): python_scripts/first_point_systems.py $(pre_with)
	python $< withDNF withSprint

pre_wo = $(HELPDICT) $(RESULTQUALIFYING) $(wDNF) $(RESULTFASTEST) $(HELPRACES) $(HELPDRIVERDATA) $(HELPPLOT)
$(TARGETwoDNF): python_scripts/first_point_systems.py $(pre_wo)
	python $< woDNF withSprint

pre_noSpwith = $(HELPDICT) $(RESULTGRID) $(RESULTwithDNF) $(RESULTFASTEST) $(HELPRACES) $(HELPDRIVERDATA) $(HELPPLOT)
$(TARGETnoSprintswithDNF): python_scripts/first_point_systems.py $(pre_noSpwith)
	python $< withDNF woSprint

pre_noSpwo = $(HELPDICT) $(RESULTQUALIFYING) $(wDNF) $(RESULTFASTEST) $(HELPRACES) $(HELPDRIVERDATA) $(HELPPLOT)
$(TARGETnoSprintswoDNF): python_scripts/first_point_systems.py $(pre_noSpwo)
	python $< woDNF woSprint

clean:
	rm -rf _includes
	rm -rf docs

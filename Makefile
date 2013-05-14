group = mcdb

#all: evolutionary_scale.gif

dist: $(group)_cooccurrence.png

evolutionary_scale.gif: evolutionary_scale.pkl plot_evolutionary_scale.py
	python plot_evolutionary_scale.py;
	convert -delay 100 -loop 0 map_*.png evolutionary_scale.gif

evolutionary_scale.pkl: evolutionary_scale.py bbs.csv bbs.new
	python evolutionary_scale.py

data/$(group)/$(group).csv: mk_csv.py $(group).sql
	python $< $(group) > $@

data/bbs/bbs.new: mk_bbs_tree.py bird.new
	python $< > $@

$(group)_distance-cooccurrence.pkl: distance.py datasets.py
	python $< $(group)

$(group)_cooccurrence.png: plot_distance.py $(group)_distance-cooccurrence.pkl
	python $< $(group)

data/$group/$(group)_traits.csv: mk_trait_csv.py $(group)_trait_query.sql $(group).sqlite
	python $< > $@

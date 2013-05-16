GROUP = mcdb

#all: evolutionary_scale.gif

dist: $(GROUP)_cooccurrence_hist_phylogenetic.png

evolutionary_scale.gif: evolutionary_scale.pkl plot_evolutionary_scale.py
	python plot_evolutionary_scale.py;
	convert -delay 100 -loop 0 map_*.png evolutionary_scale.gif

evolutionary_scale.pkl: evolutionary_scale.py bbs.csv bbs.new
	python evolutionary_scale.py

data/$(GROUP)/$(GROUP).csv: mk_csv.py $(GROUP).sql
	python $< $(GROUP) > $@

data/bbs/bbs.new: mk_bbs_tree.py bird.new
	python $< > $@

$(GROUP)_distance-cooccurrence.pkl: distance.py datasets.py
	python $< $(GROUP)

$(GROUP)_cooccurrence.png: plot_distance.py $(GROUP)_distance-cooccurrence.pkl
	python $< $(GROUP)

data/$GROUP/$(GROUP)_traits.csv: mk_trait_csv.py $(GROUP)_trait_query.sql $(GROUP).sqlite
	python $< > $@

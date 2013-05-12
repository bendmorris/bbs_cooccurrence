all: evolutionary_scale.gif

dist: cooccurrence.png

evolutionary_scale.gif: evolutionary_scale.pkl plot_evolutionary_scale.py
	python plot_evolutionary_scale.py;
	convert -delay 100 -loop 0 map_*.png evolutionary_scale.gif

evolutionary_scale.pkl: evolutionary_scale.py bbs.csv bbs.new
	python evolutionary_scale.py

bbs.csv: mk_csv.py query.sql bbs.sqlite
	python $< > $@

bbs.new: mk_bbs_tree.py bird.new
	python mk_bbs_tree.py > bbs.new

distance-cooccurrence.pkl: distance.py
	python distance.py

cooccurrence.png: plot_distance.py distance-cooccurrence.pkl
	python plot_distance.py

bbs_body_size.csv: mk_bbs_body_size_csv.py bbs_body_size_query.sql bbs.sqlite
	python $< > $@

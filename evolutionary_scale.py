from pylab import *
from granivore_dict import granivore_dict
import Bio.Phylo as bp
from geophy.cluster import color_clusters
import numpy
import csv
import cPickle as pkl


tree = bp.read('fia.new', 'newick')
tips = tree.get_terminals()
all_species = {t.name: t for t in tips}

routes = {}
with open('fia.csv') as data_file:
    reader = csv.reader(data_file)
    reader.next()
    for lat, lon, genus, species, count in reader:
        spname = '%s %s' % (genus, species)
        if not spname in all_species: continue
        lat, lon = round(float(lat)), round(float(lon))
        count = int(count)
        route = lat, lon
        if not route in routes: routes[route] = set()
        routes[route].add(spname)

results = {}
for threshold in np.arange(0, 40, 5):
    print threshold
    results[threshold] = {}
    color_clusters(tree, threshold=threshold, draw=False, all_colors = xrange(len(tips)),
                   color_attr='group', min_clade_size=1)
    for route, spp in routes.iteritems():
        results[threshold][route] = set()
        for sp in spp:
            if sp in all_species and hasattr(all_species[sp], 'group'):
                results[threshold][route].add(all_species[sp].group)

with open('evolutionary_scale.pkl', 'w') as pickle_file:
    pkl.dump(results, pickle_file, -1)

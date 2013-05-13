from granivore_dict import granivore_dict
import Bio.Phylo as bp
import csv
import cPickle as pkl
import numpy as np
import sys
from datasets import datasets

try: group = sys.argv[1]
except: group = 'bbs'

dataset = datasets[group]


tree = bp.read('%s.new' % group, 'newick')

traits = {}
with open('%s_traits.csv' % group) as data_file:
    reader = csv.reader(data_file)
    reader.next()
    for line in reader:
        sp = line[0]
        traits[sp] = ()
        for n, t in enumerate(line[1:]):
            try:
                t = float(t)
                if dataset['log_traits'][n]: t = np.log(t)
            except: t = None
            traits[sp] = traits[sp] + (t,)

distance_dict = {}
def distance(*spp):
    assert len(spp) == 2
    a, b = [s.replace('_', ' ') for s in sorted(spp)]
    if not (a,b) in distance_dict:
        try: distance_dict[a,b] = tree.distance(birds[a], birds[b])
        except KeyError: return None
    return distance_dict[a,b]

birds = {t.name: t for t in tree.get_terminals()}

routes = {}
spp_seen = set()
with open('bbs.csv') as data_file:
    reader = csv.reader(data_file)
    reader.next()
    for lat, lon, genus, species, count in reader:
        sp_name = '%s %s' % (genus, species)
        if not sp_name in birds: continue
        route = float(lat), float(lon)
        if not route in routes: routes[route] = set()
        routes[route].add(sp_name)
        spp_seen.add(sp_name)

ys = []
xs = []
all_c = []
for sp1 in spp_seen:
    if not (sp1 in birds and sp1 in traits and all(traits[sp1])): continue
    for sp2 in spp_seen:
        if sp2 <= sp1: continue
        if not (sp2 in birds and sp2 in traits and all(traits[sp2])): continue

        routes1 = set([route for route in routes if sp1 in routes[route]])
        routes2 = set([route for route in routes if sp2 in routes[route]])

        cooccurrence = len(routes1.intersection(routes2)) / float(len(routes1.union(routes2)))
        dist = distance(sp1, sp2)

        trait_diffs = [abs(traits[sp1][n] - traits[sp2][n]) for n in range(len(traits[sp1]))]
        
        all_c.append((sp1, sp2, cooccurrence, dist,) + tuple(trait_diffs))

        ys.append(cooccurrence)
        xs.append(dist)


#points = zip(xs, ys)
#def kde(x, k=1):
#    l = []
#    weights = []
#    for px, py in points:
#            l.append(py)
#            weights.append(1. / (abs(x - px) ** k))
#    return sum([li * w for li, w in zip(l, weights)] / sum(weights))

#hexbin(xs, ys, bins='log')
#xm = arange(min(xs), max(xs), 1)
#plot(xm, [kde(x) for x in xm])
#savefig('cooccurrence.png')


with open('%s_distance-cooccurrence.pkl' % group, 'w') as output_file:
    pkl.dump(all_c, output_file, -1)


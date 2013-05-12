from pylab import *
import cPickle as pickle
import Bio.Phylo as bp
import sys

tree = bp.read('bird.new', 'newick')

data = pickle.load(open('data.pkl'))
regions = data['regions']
routes = data['routes']

xs = []
ys = []
all_counts = {}
dists = {}
for region in regions:
    print 'region', region
    # add up abundances of all species found in this conservation region
    all_counts[region] = {}
    counts = regions[region]
    for count in counts:
        for species in counts[count]:
            if not species in all_counts[region]: all_counts[region][species] = 0
            all_counts[region][species] += counts[count][species]

    print len(all_counts[region]), 'species',
    sys.stdout.flush()

    # compute species-level and individual-level diversity metrics for region
    species = sorted(all_counts[region].keys())
    x = []
    y = []
    y_weights = []
    for (i, s1) in enumerate(species):
        for s2 in species[i:]:
            if not (s1, s2) in dists: dists[(s1, s2)] = tree.distance(s1, s2)
            dist = dists[(s1, s2)]
            if s1 != s2: x.append(dist)
            y.append(dist)
            y_weights.append(all_counts[region][s1] * all_counts[region][s2])

    x = mean(x)
    y = sum([yi * w for yi, w in zip(y, y_weights)]) / sum(y_weights)
    xs.append(x)
    ys.append(y)
    print 'x=%s y=%s' % (x, y)
    
data2 = {}
for x in 'regions', 'xs', 'ys':
    data2[x] = eval(x)
pickle.dump(data2, open('data2.pkl', 'w'))
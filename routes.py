from pylab import *
import Bio.Phylo as bp
import sqlite3 as dbapi
import csv
import sys
import cPickle as pickle

syn_groups = []
r = csv.reader(open('bird_syns.csv'))
for i in range(2): r.next()
for line in r:
    if not line: continue
    name, syns = line[3], line[21]
    if syns:
        syns = [name] + [s.split('(')[0].strip() for s in syns.split(';')][:-1]
        syns = [syn.replace(' ', '_') for syn in syns]
        syn_groups.append(set(syns))

tree = bp.read('bird.new', 'newick')

terminals = set([n.name for n in tree.get_terminals()])

syns = {
'Cardellina_pusilla':'Wilsonia_pusilla',
'Corvus_cora':'Corvus_corax',
'Acanthis_flammea':'Carduelis_flammea',
'Gallinago_delicata': 'Gallinago_gallinago',
'Helmintophila_celata': 'Vermivora_celata',
'Oreothlypis_celata': 'Vermivora_celata',
'Carpodacus_me': 'Carpodacus_mexicanus',
'Melanitta_americana':'Melanitta_nigra',
'Thalasseus_ma':'Sterna_maxima',
}

con = dbapi.connect('bbs.db')
cur = con.cursor()
cur.execute('''SELECT s.genus, s.species, s.AOU
FROM BBS_species s
WHERE s.genus IS NOT NULL
AND s.species IS NOT NULL''')

def convert_name(genus, species):
    for joiner in ('x', ' or ', '/'):
        species = species.split(joiner)[0].strip()
    n = '%s_%s' % (genus, species)
    if n in syns: return syns[n]
    return n

aous = {}
for genus, species, aou in cur:
    full_name = convert_name(genus, species)
    aous[aou] = full_name
bbs_species_names = set(aous.values())

granivores = set()
for filename in ('granivores.csv', 'partial_granivores.csv'):
    with open(filename) as input_file:
        for line in input_file:
            granivores.add(int(line.split(',')[-1].strip()))

known_species = bbs_species_names.intersection(terminals)
unknown_species = bbs_species_names.difference(terminals)
for sp in unknown_species.copy():
    for syn_group in syn_groups:
        if sp in syn_group:
            for syn in syn_group:
                if syn in terminals:
                    syns[sp] = syn
                    unknown_species.remove(sp)
                    known_species.add(syn)
                    break
    if sp in unknown_species:
        for sp2 in terminals:
            if sp.split('_')[0] == sp2.split('_')[0] or sp.split('_')[1] == sp2.split('_')[1]:
                syns[sp] = sp2
                unknown_species.remove(sp)
                known_species.add(sp2)
                break

print 'BBS species present in tree: %s' % len(known_species)
print 'BBS species not present in tree: %s' % len(unknown_species)
print unknown_species

cur.execute('''
SELECT SUM(c.SpeciesTotal), COUNT(c.year), c.Aou, c.countrynum, c.statenum, c.route, r.lati, r.loni, r.bcr
FROM bbs_counts c
JOIN bbs_routes r
ON (c.countrynum = r.countrynum and c.statenum = r.statenum
    and c.Route = r.Route)
WHERE c.year >= 2006 and c.year <= 2010
GROUP BY c.countrynum, c.statenum, c.Route, c.Aou
''')

regions = {}
routes = {}
for total, years, aou, country, state, route, lat, lon, bcr in cur:
    if years < 5: continue
    if not aou in granivores: continue
    if not bcr in regions: regions[bcr] = {}
    route = '%s-%s-%s' % (country, state, route)
    try: name = aous[aou]
    except KeyError: continue
    if name in syns: name = syns[name]
    counts = regions[bcr]
    if not route in routes: routes[route] = (lat, lon)
    if not route in counts: counts[route] = {}
    counts[route][name] = round(total/float(years), 2)

print len(regions), 'regions'

# average phylogenetic distance:
#   x is species-based
#   y is individual-based
dists = {}
xs = []
ys = []
zs = []
for region in regions:#.keys()[:1]:
    print 'region %s' % region
    counts = regions[region]
    print '%s routes' % len(counts)
    
    for route in counts:
        print '\troute %s,' % route,
        bad_route = False

        these_counts = counts[route]
        if len(these_counts) < 2: continue
        species = sorted(these_counts.keys())
        print len(species), 'species',
        sys.stdout.flush()
        x = []
        y = []
        y_weights = []

        for i, n in enumerate(species):
            if n in syns: n = syns[n]
            if bad_route: break
            for m in species[i:]:
                if m in syns: m = syns[m]
                if m in unknown_species:
                    bad_route = True
                    print 'bad route:', route, m
                    break
                if not (n, m) in dists: dists[(n,m)] = tree.distance(n, m)
                dist = dists[(n,m)]
                if n != m: x.append(dist)
                y.append(dist)
                y_weights.append(these_counts[n] * these_counts[m])

        if bad_route: continue
        x = mean(x)
        y = sum([yi * w for yi, w in zip(y, y_weights)]) / sum(y_weights)
        xs.append(x)
        ys.append(y)
        zs.append((region, routes[route]))
        print 'x=%s y=%s' % (x,y)

data = {}
for n in ('regions', 'routes', 'xs', 'ys', 'zs'):
    data[n] = eval(n)
pickle.dump(data, open('data.pkl', 'w'))

scatter(xs, ys)
show()
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
name_to_aou = {}
for genus, species, aou in cur:
    full_name = convert_name(genus, species)
    aous[aou] = full_name
    name_to_aou[full_name] = aou
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
print 'granivores: %s' % len(granivores)
print {aou:convert_name(*name.split('_')) for aou,name in aous.items() if aou in granivores}
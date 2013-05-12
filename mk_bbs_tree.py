import csv
import Bio.Phylo as bp

t = bp.read('bird.new', 'newick')

spp = set()
with open('bbs.csv') as input_file:
    reader = csv.reader(input_file)
    reader.next()
    for lat, lon, genus, species, count in reader:
        sp = '%s %s' % (genus, species)
        spp.add(sp)

terms = t.get_terminals()
for x in terms:
    if x.name:
        x.name = x.name.replace('_', ' ')
        if not x.name in spp: t.prune(x)

terms = t.get_terminals()
while len([x for x in terms if not x.name]):
    for x in terms:
        if not x.name: t.prune(x)
    terms = t.get_terminals()

print t.format('newick')
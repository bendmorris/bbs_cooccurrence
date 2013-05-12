import Bio.Phylo as bp
import geophy.cluster as g
import sys

try: tree_file = sys.argv[1]
except: tree_file = 'bbs_granivores.new'

t = bp.read(tree_file,'newick')

g.color_clusters(t, threshold=10)
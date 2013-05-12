from pylab import *
import Bio.Phylo as bp
import random

species_level = True
repetitions = 100
community_size = 16
num_communities = 100

comm_diversity_ratios = []
comm_weights = []

tree = bp.read('bird.new', 'newick')
all_species = [s.name for s in tree.get_terminals()]

distances = {}

for i in range(repetitions):
    species = random.sample(all_species, random.randint(community_size/2, community_size*2))
    print species

    communities = [[random.choice(species) for i in range(community_size)]
                    for j in range(num_communities)]

    for timestep in range(1000):
        for community in communities:
            community[random.randint(0, len(community)-1)] = random.choice(list(species) + community)
    
    regional_diversity = []
    weights = []
    inds = [ind for community in communities for ind in community]
    for i, s1 in enumerate(species):
        for s2 in (species[i+1:]):
            s = tuple(sorted((s1, s2)))
            if not s in distances: distances[s] = tree.distance(s1, s2)
            distance = distances[s]
            print s1, s2, distance
            regional_diversity.append(distance)
            if not species_level: weights.append(inds.count(s1) * inds.count(s2))
    if species_level: regional_diversity = mean(regional_diversity)
    else: regional_diversity = sum([r * w for (r, w) in zip(regional_diversity, weights)]) / sum(weights)

    for community in communities:
        comm_diversity = []
        this_community = list(set(community))
        for i, s1 in enumerate(this_community):
            for s2 in this_community[i+1:]:
                s = tuple(sorted((s1, s2)))
                if not s in distances: distances[s] = tree.distance(s1, s2)
                distance = distances[s]
                comm_diversity.append(distance)
                comm_weights.append(community.count(s1) * community.count(s2))
        if species_level: comm_diversity = mean(comm_diversity)
        else: comm_diversity = sum([c * w for (c, w) in zip(comm_diversity, comm_weights)]) / sum(comm_weights)
        ratio = comm_diversity / regional_diversity
        #print len(this_community), round(comm_diversity, 2), round(regional_diversity, 2)
        comm_diversity_ratios.append(ratio)

xlabel('local diversity / regional diversity')
hist(comm_diversity_ratios, bins=100, range=(0,1.5), normed=True)
ylim(0,8)

show()

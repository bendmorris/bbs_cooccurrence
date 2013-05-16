import cPickle as pkl
import numpy as np
import matplotlib.pyplot as plt
import sys
from datasets import datasets

try: group = sys.argv[1]
except: group = 'bbs'

dataset = datasets[group]
trait_names = dataset['traits']


HIGH_COOCCURRENCE_THRESHOLD = 0.5
BINS = 20
tuple_pos = {x:n+3 for n, x in enumerate(('phylogenetic',) + trait_names)}

with open('%s_distance-cooccurrence.pkl' % group) as pkl_file:
    all_c = pkl.load(pkl_file)

    no_c = [x for x in all_c if x[2] == 0]
    hi_c = [x for x in all_c if x[2] >= HIGH_COOCCURRENCE_THRESHOLD]

for VARIABLE in tuple_pos:
    USE = tuple_pos[VARIABLE]

    # histograms
    plt.figure()
    plt.title('%s %s: histograms' % (group, VARIABLE))

    distances = [x[USE] for x in all_c]
    bins = np.linspace(min(distances), max(distances), BINS+1)

    max_height = 0

    for label, data in (
            ('no co-occurrence', no_c),
            ('>%s%% co-occurrence' % int(HIGH_COOCCURRENCE_THRESHOLD*100), hi_c),
            #('all species pairs', all_c),
            ):
        data = [x[USE] for x in data]
        pdf, bins, _ = plt.hist(data, bins, normed=True, alpha=0.5, label=label, histtype='stepfilled')
        
        max_height = max([max_height] + pdf)
    
    plt.ylim(0, max_height)
    plt.xlabel('%s distance' % VARIABLE)
    plt.ylabel('proportion of species pairs')
    plt.legend(loc='upper left')
    plt.savefig('%s_cooccurrence_hist_%s.png' % (group, VARIABLE))


    # histogram differences
    
    plt.figure()
    plt.title('%s %s: differences' % (group, VARIABLE))

    for label, data in (
            ('no co-occurrence', no_c),
            ('>%s%% co-occurrence' % int(HIGH_COOCCURRENCE_THRESHOLD*100), hi_c),
    ):
        data1 = [x[USE] for x in data]
        data2 = [x[USE] for x in all_c]
        digs1 = np.digitize(data1, bins)
        digs2 = np.digitize(data2, bins)
        data1 = np.array([len(digs1[digs1==b])/float(len(data1)) for b in range(len(bins))])
        data2 = np.array([len(digs2[digs2==b])/float(len(data2)) for b in range(len(bins))])
        plt.plot(bins, data1 - data2, label=label)
    
    plt.plot(bins, [0 for b in bins])
    
    plt.legend(loc='upper right')
    plt.xlabel('%s distance' % VARIABLE)
    plt.ylabel('difference: high vs. no co-occurrence')

    plt.savefig('%s_cooccurrence_diff_%s.png' % (group, VARIABLE))


    # Q-Q plot
    plt.figure()
    plt.title('%s %s: Q-Q' % (group, VARIABLE))
    
    x_data = np.array(sorted([x[USE] for x in no_c]))
    y_data = np.array(sorted([x[USE] for x in hi_c]))
    xs = []
    ys = []
    for i in np.arange(0, 100, 0.5):
        x = np.percentile(x_data, i)
        y = np.percentile(y_data, i)
        xs.append(x)
        ys.append(y)

    plt.plot(xs, ys)
    plt.plot([0,max(xs+ys)],[0,max(xs+ys)])
    plt.xlabel('no co-occurrence')
    plt.ylabel('>%s%% co-occurrence' % int(HIGH_COOCCURRENCE_THRESHOLD * 100))
    
    plt.savefig('%s_cooccurrence_qq_%s.png' % (group, VARIABLE))

#plt.show()

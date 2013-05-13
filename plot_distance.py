import cPickle as pkl
import numpy as np
import matplotlib.pyplot as plt


HIGH_COOCCURRENCE_THRESHOLD = 0.1
BINS = 10
tuple_pos = {'phylogenetic':3, 'body size':4, 'bill size':5}

with open('distance-cooccurrence.pkl') as pkl_file:
    all_c = pkl.load(pkl_file)

    no_c = [x for x in all_c if x[2] == 0]
    hi_c = [x for x in all_c if x[2] >= HIGH_COOCCURRENCE_THRESHOLD]

for VARIABLE in tuple_pos:
    USE = tuple_pos[VARIABLE]

    # histograms
    plt.figure()


    distances = [x[2] for x in all_c]
    bins = np.linspace(min(distances), max(distances), BINS+1)

    for label, dataset in (
            ('no cooccurrence', no_c),
            ('>%s%% cooccurrence' % int(HIGH_COOCCURRENCE_THRESHOLD*100), hi_c),
            #('all species pairs', all_c),
            ):
        data = [x[USE] for x in dataset]
        n, b, patches = plt.hist(data, bins, normed=True, alpha=0.5, label=label, 
                                 histtype='stepfilled')
        print n, b, patches

    plt.xlabel('%s distance' % VARIABLE)
    plt.ylabel('proportion of species pairs')
    plt.legend(loc='upper left')
    plt.savefig('cooccurrence_hist_%s.png' % VARIABLE)


    # Q-Q plot
    plt.figure()
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
    plt.xlabel('no cooccurrence')
    plt.ylabel('>%s%% cooccurrence' % int(HIGH_COOCCURRENCE_THRESHOLD * 100))

    plt.savefig('cooccurrence_qq_%s.png' % VARIABLE)

plt.show()

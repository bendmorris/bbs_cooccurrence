from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import cPickle as pkl


x_shift, y_shift = 0,0

with open('evolutionary_scale.pkl') as pickle_file:
    results = pkl.load(pickle_file)

lats = set([route[0]
        for threshold, result in results.iteritems()
        for route in result.iterkeys()])
lons = set([route[1]
        for threshold, result in results.iteritems()
        for route in result.iterkeys()])

print min(lats), max(lats)
print min(lons), max(lons)
xs = np.array(sorted(lons))
ys = np.array(sorted(lats))
x, y = np.meshgrid(xs, ys)

cdict = {'red':   [(0.0,  1.0, 1.0),
                   (0.25, 0.0, 0.0),
                   (0.5,  0.0, 0.0),
                   (0.75, 1.0, 1.0),
                   (1.0,  1.0, 1.0)],

         'green': [(0.0,  1.0, 1.0),
                   (0.25, 0.0, 0.0),
                   (0.5,  1.0, 1.0),
                   (0.75, 1.0, 1.0),
                   (1.0,  0.0, 0.0)],

         'blue':  [(0.0,  1.0, 1.0),
                   (0.25, 1.0, 1.0),
                   (0.5,  0.0, 0.0),
                   (0.75, 0.0, 0.0),
                   (1.0,  0.0, 0.0)]}
cmap = colors.LinearSegmentedColormap('cmap', cdict)

for threshold in sorted(results.keys()):
    print threshold
    result = results[threshold]

    plt.figure()
    map = Basemap(llcrnrlon=min(lons)+x_shift,llcrnrlat=min(lats)+y_shift,
                  urcrnrlon=max(lons)+x_shift,urcrnrlat=max(lats)+y_shift,
                  projection='merc',lat_1=33,lat_2=45,lon_0=-95,resolution='l')

    map.drawcoastlines(linewidth=1)
    map.drawcountries(linewidth=1)
    map.drawstates(linewidth=0.5)

    #xs = []
    #ys = []
    #zs = []
    #for (lat, lon), spp in result.iteritems():
    #    x, y = map(lon, lat)
    #    xs.append(x)
    #    ys.append(y)
    #    zs.append(len(spp))
    #print xs, ys, zs
    #map.scatter(xs, ys, zs)
    
    data = np.zeros(x.shape)
    for i in xrange(x.shape[0]):
        for j in xrange(x.shape[1]):
            try: data[i,j] = len(result[y[i][j],x[i][j]])
            except KeyError: data[i,j] = 0
    
    map.pcolormesh(x+x_shift, y+y_shift, data=data, latlon=True,
                   cmap=cmap)
    cbar = plt.colorbar()
    plt.title(str(threshold)+'th percentile')

    plt.savefig('map_%s.png' % str(int(threshold*10)).zfill(3))
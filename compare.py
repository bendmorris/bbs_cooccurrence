from pylab import *
import cPickle as pickle


data = pickle.load(open('data.pkl'))
data2 = pickle.load(open('data2.pkl'))

regions = {}
for r, x, y in zip(data2['regions'], data2['xs'], data2['ys']):
    regions[r] = (x, y)

xs = []
ys = []
for x, y, (r, (lat, lon)) in zip(data['xs'], data['ys'], data['zs']):
    rx, ry = regions[r]
    xs.append(x / rx)
    ys.append(y / ry)

#scatter(xs, ys)
xlabel('local diversity / regional diversity')
hist(xs, bins=100, range=(0,1.5), normed=True)
ylim(0,8)
show()
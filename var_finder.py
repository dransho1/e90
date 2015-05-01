import matplotlib.pyplot as plt
import matplotlib.patches as ptch
import numpy as np

MEASURED_POSITIONS = {1: (-.6096,-2.135,90),
        2: (1.524,-2.4384,90),
        3: (.3048,-1.524,90),
        4: (1.524,.6096,90),
        5: (.6096,1.524,90),
        6: (0,1.8288,90),
        7: (.6096,3.3528,90),
        8: (.9244,4.2672,90),
        }

def clean(f):
    dirty = [line for line in f]
    data = dirty[2:] # get rid of file headers
    location_points = [data[i].split() for i in range(3, len(data), 2)]
    loc_data = [[float(p) for p in point] for point in location_points]
    return loc_data

def get_params(data, pos):
    x_s = [datum[0] for datum in data]
    y_s = [datum[1] for datum in data] 
    plt.plot(x_s, y_s, 'ro')
    plt.plot(pos[0], pos[1], 'bo')
    plt.plot(10,10,'go')
    plt.axis([5,15,5,15])
    rp = ptch.Patch(color='red', label='Measurements')
    bp = ptch.Patch(color='blue', label='Actual position')
    gp = ptch.Patch(color='green', label='World origin')
    plt.legend(handles=[rp,bp,gp])
    plt.show()
    return np.cov(x_s, y_s), [np.mean(x_s), np.mean(y_s)]

def main():
    params = []
    errors = []
    sampled = [1,2,3,4,5]
    for fnum in sampled:
        pos = MEASURED_POSITIONS[fnum]
        pos_adj = [pos[0]+10, pos[1]+10, pos[2]] # adjust for origin offset
        f = open('location_{}.txt'.format(fnum), 'r')
        data = clean(f)
        cov, mean = get_params(data, pos_adj)
        params.append([cov, mean])
        errors.append([abs(mean[0]-pos_adj[0]), abs(mean[1]-pos_adj[1])])

    print "paramters", params
    print "errors", errors

main()
#print [(i,[l+10 for l in MEASURED_POSITIONS[i]]) for i in MEASURED_POSITIONS]

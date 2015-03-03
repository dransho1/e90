import numpy as np
import graphics as gr
import random, math, time 
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.optimize import minimize, check_grad, approx_fprime
from mpl_toolkits.mplot3d import Axes3D

MIRROR_RADIUS = 30 #mm

BEACON_LOCS = {
        'red':(10,10,'red'),
        'green':(680,100, 'green'),
        'blue':(350,680, 'blue')
        }


def project(beacons, disk, df):
    projections = []
    for (beacon,color) in beacons:
        bc_pt = beacon.getCenter()
        d_pt = disk.getCenter()
        x_comp = d_pt.getX() - bc_pt.getX()
        y_comp = d_pt.getY() - bc_pt.getY()
        r = np.sqrt(x_comp**2 + y_comp**2)
        projected_beacon = gr.Circle(gr.Point(-MIRROR_RADIUS*x_comp/r + d_pt.getX(),
                                              -MIRROR_RADIUS*y_comp/r + d_pt.getY()),
                                     3)

        projected_beacon.setFill(color)
        projections.append((projected_beacon, color))
    return projections

def alpha(x, y, theta, bcn_x, bcn_y):
    angle = np.arctan2(bcn_y-y, bcn_x-x)-theta
    return angle

def guess_position_from(angles, init_guess=None):
    '''
    The most important function in this script - generates a guess for the
    position based on the beacon locations and the angles to the beacon
    '''
    error_fun = lambda x : np.sum([(angles[color]-alpha(x[0],x[1],x[2],\
            BEACON_LOCS[color][0], BEACON_LOCS[color][1]))**2 \
            for color in angles])
    grad = lambda x : np.array(jacobian(x[0],x[1],x[2],angles))
    if init_guess is None:
        guess = [400,400,0]
    else:
        guess = init_guess
    bnds = ((0,800), (0,800), (-2*3.14159, 2*3.14159))
    result = minimize(error_fun, guess, jac=grad, method='TNC', bounds=bnds)    
    #result = minimize(error_fun, guess, jac=grad, method='BFGS', bounds=bnds)
    return result.x

def dx(x,y,t,bx,by):
    #the derivative of atan2(x,y) with respect to x
    X = float(bx-x)
    Y = float(by-y)
    return (1*Y)/(X**2 + Y**2)

def dy(x,y,t,bx,by):
    X = float(bx-x)
    Y = float(by-y)
    var = ((-X)/(X**2 + Y**2))
    return var

def dt(x,y,t,bx,by):
    return -1

def d_sse(a,x,y,t,bx,by, d):
    var =  -2*(a-alpha(x,y,t,bx,by))*d(x,y,t,bx,by)
    return var

def jacobian(x,y,t,angles):
    b = BEACON_LOCS
    J = [sum([d_sse(angles[i],x,y,t,b[i][0],b[i][1],dx) for i in angles]),
        sum([d_sse(angles[i],x,y,t,b[i][0],b[i][1],dy) for i in angles]),
        sum([d_sse(angles[i],x,y,t,b[i][0],b[i][1],dt) for i in angles])]
    return J

def main():
    positioning_errors = np.zeros((62,62))
    angle_sigmas = [np.radians(1),
            np.radians(2),
            np.radians(5),
            np.radians(8),
            np.radians(10),
            np.radians(25),
            ]
    print "Calculating positioning errors..."
    xs = range(1,800,13)
    ys = range(1,800,13)
    try:
        print("searching for files")
        one_s = np.load('pe1.npy')
        two_s = np.load('pe2.npy')
        five_s = np.load('pe5.npy')
        eight_s = np.load('pe8.npy')
        ten_s = np.load('pe10.npy')
        twenty_five_s = np.load('pe25.npy')
    except IOError:
        print("couldn't load all stats, recalculating")
        for angle_sigma in angle_sigmas:
            for i,x in enumerate(xs):
                for j,y in enumerate(ys):
                    disk_x = x#random.randint(100,300)
                    disk_y = y#random.randint(100,300)
                    disk_t = random.uniform(0,2*3.14159)
                    disk = gr.Circle(gr.Point(disk_x, disk_y), MIRROR_RADIUS)
                    disk_front = gr.Point(MIRROR_RADIUS*math.cos(disk_t)+disk_x, 
                                            MIRROR_RADIUS*math.sin(disk_t)+disk_y)
                    #print("True Center at ({}, {})".format(disk_x, disk_y))
                    #print("True bearing is {}".format(np.degrees(disk_t)))
                    nose = gr.Circle(disk_front, 5)
                    beacons = []
                    for beacon_spec in BEACON_LOCS.values():
                        beacon = gr.Circle(gr.Point(beacon_spec[0], beacon_spec[1]),7)
                        beacon.setFill(beacon_spec[2])
                        beacons.append((beacon, beacon_spec[2]))
                    projections = project(beacons, disk, disk_front)

                    angles = {}
                            
                    for color,ptcolor in BEACON_LOCS.iteritems():
                            angles[color] = alpha(disk_x, disk_y, disk_t, 
                                ptcolor[0], ptcolor[1]) + np.random.normal(scale=angle_sigma)

                    init_guess = np.array([disk_x, disk_y, disk_t]) 
                    pos_guess = guess_position_from(angles, init_guess)
                    error = pos_guess - [disk_x, disk_y, disk_t]
                    positioning_errors[i][j] = np.linalg.norm(error)
            np.save('pe{}.npy'.format(int(np.degrees(angle_sigma))), positioning_errors)
        main()
    fig = plt.figure()
    X,Y = np.meshgrid(xs,ys)
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X,Y,two_s, cmap=cm.coolwarm)
    plt.show()
    errs = []
    vals = []
    for err, mat in ((1,one_s), (2,two_s), (5,five_s), (8,eight_s), (10,ten_s), (25, twenty_five_s)):
        print "average positioning error:", np.mean(mat)
        errs.append(err)
        vals.append(np.mean(mat))
        print "average positioning error near center:", np.mean(mat[30:35,30:35])
    fig = plt.figure()
    plt.plot(errs,vals)
    plt.show()

    ##### error as a function of distance from each beacon #####
main()

import numpy as np
import graphics as gr
import random, math, time 
from scipy.optimize import minimize, check_grad, approx_fprime

MIRROR_RADIUS = 30 #mm

BEACON_LOCS = {
        'red':(.52,7.04,'red'),
        'green':(2.17,-3.05, 'green'),
        'blue':(-1.65,-5.34, 'blue')
        }


def alpha(x, y, theta, bcn_x, bcn_y):
    angle = np.arctan2(bcn_y-y, bcn_x-x)-theta
    return angle

def guess_position_from(angles, init_guess=None):
    '''
    The most important function in this script - generates a guess for the
    position based on the beacon locations and the angles to the beacon
    '''
    # x[0] is x, x[1] is y, x[2] = theta
    error_fun = lambda x : np.sum([(angles[color]-alpha(x[0],x[1],x[2],\
            BEACON_LOCS[color][0], BEACON_LOCS[color][1]))**2 \
            for color in angles])
    grad = lambda x : np.array(jacobian(x[0],x[1],x[2],angles))
    if init_guess is None:
        guess = [0.0,0.0,0]
    else:
        guess = init_guess
    bnds = ((0,20), (0,20), (-2*3.14159, 2*3.14159))
    result = minimize(error_fun, guess, method='TNC', bounds=bnds)    
    return result.x

def dx(x,y,t,bx,by):
    #the derivative of atan2(y,x) with respect to x
    X = float(bx-x)
    Y = float(by-y)
    return (Y)/(X**2 + Y**2)

def dy(x,y,t,bx,by):
    X = float(bx-x)
    Y = float(by-y)
    var = (-X)/(X**2 + Y**2)
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



import numpy as np
import graphics as gr
import random, math, time 
from scipy.optimize import minimize, check_grad, approx_fprime
MIRROR_RADIUS = 30 #mm
BEACON_LOCS = {
        'red':(10,10,'red'),
        'green':(680,100, 'green'),
        'blue':(350,680, 'blue')
        }

def find_angle_between(disk, projections, df):
    disk_center_offset_x = disk.getCenter().getX()
    disk_center_offset_y = disk.getCenter().getY()
    #account for the fact that our graphics live in world frame
    angle_for = {}
    vector_of_front = np.array([
        df.getX() - disk_center_offset_x,
        df.getY() - disk_center_offset_y
        ])
    reference_vec = [0,-1*MIRROR_RADIUS]
    true_bearing = np.arccos((1.0/(MIRROR_RADIUS**2))*\
            vector_of_front.dot(reference_vec))
    sign = np.sign(np.cross(vector_of_front, reference_vec))
    print("True bearing: {}".format(np.degrees(true_bearing*sign)))
    for dot, color in projections:
        vector = np.array([
            dot.getCenter().getX() - disk_center_offset_x,
            dot.getCenter().getY() - disk_center_offset_y
            ])
        sign = np.sign(np.cross(vector, vector_of_front))
        angle_for[color] = sign*np.arccos((1.0/(MIRROR_RADIUS**2))*\
                vector_of_front.dot(vector))
    return angle_for

def project(beacons, disk, df):
    projections = []
    for (beacon,color) in beacons:
        bc_pt = beacon.getCenter()
        d_pt = disk.getCenter()
        x_comp = d_pt.getX() - bc_pt.getX()
        y_comp = d_pt.getY() - bc_pt.getY()
        ang = np.arctan2(y_comp, x_comp)
        ang -= np.pi
        projected_beacon = gr.Circle(gr.Point(MIRROR_RADIUS*math.cos(ang)
            + d_pt.getX(), MIRROR_RADIUS*math.sin(ang)+d_pt.getY()), 3)
        projected_beacon.setFill(color)
        projections.append((projected_beacon, color))
    return projections

def alpha(x, y, theta, bcn_x, bcn_y):
    angle = np.arctan2(x-bcn_x, y-bcn_y)-theta
    return angle

def guess_position_from(angles):
    '''
    The most important function in this script - generates a guess for the
    position based on the beacon locations and the angles to the beacon
    '''
    # x[0] is x, x[1] is y, x[2] = theta
    error_fun = lambda x : np.sum([(angles[color]-alpha(x[0],x[1],x[2],\
            BEACON_LOCS[color][0], BEACON_LOCS[color][1]))**2 \
            for color in angles])
    grad = lambda x : np.array(jacobian(x[0],x[1],x[2],angles))
    guess = [100,100,1]
    bnds = ((0,800), (0,800), (-2*3.14159, 2*3.14159))
    result = minimize(error_fun, guess, jac=grad, method='TNC', bounds=bnds)    
    #result = minimize(error_fun, guess, jac=grad, method='BFGS', bounds=bnds)
    #print result
    eps = np.sqrt(np.finfo(np.float).eps)
    #print approx_fprime(guess, error_fun, eps)
    #print jacobian(guess[0],guess[1],guess[2],angles)
    return result.x

def dx(x,y,t,bx,by):
    #the derivative of atan2(x,y) with respect to x
    X = float(bx-x)
    Y = float(by-y)
    return (-1*Y)/(X**2 + Y**2)

def dy(x,y,t,bx,by):
    X = float(bx-x)
    Y = float(by-y)
    var = ((X)/(X**2 + Y**2))
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
    sim_window = gr.GraphWin('Simulation', 800,800)
    disk_x = random.randint(100,300)
    disk_y = random.randint(100,300)
    while True:
        disk_t = random.uniform(0,2*3.14159)
        #disk_t = np.radians(deg)
        disk = gr.Circle(gr.Point(disk_x, disk_y), MIRROR_RADIUS)
        disk_front = gr.Point(MIRROR_RADIUS*math.cos(disk_t)+disk_x, 
                MIRROR_RADIUS*math.sin(disk_t)+disk_y)
        print("True Center at ({}, {})".format(disk_x, disk_y))
        disk.setFill("gray")
        disk.draw(sim_window)
        nose = gr.Circle(disk_front, 5)
        nose.draw(sim_window)
        beacons = []
        for beacon_spec in BEACON_LOCS.values():
            beacon = gr.Circle(gr.Point(beacon_spec[0], beacon_spec[1]),7)
            beacon.setFill(beacon_spec[2])
            beacon.draw(sim_window)
            beacons.append((beacon, beacon_spec[2]))
        projections = project(beacons, disk, disk_front)
        for p,c in projections:
            p.draw(sim_window)
        angles =  find_angle_between(disk, projections, disk_front)
        for dot_color in angles:
            print("Angle to {} is {} degrees".format(dot_color,
                np.degrees(angles[dot_color])))
        pos_guess = guess_position_from(angles)
        print("I guess my position to be ({}, {}) with orientation {}".format(
            pos_guess[0], pos_guess[1], np.degrees(pos_guess[2])))
        new_point = sim_window.getMouse()
        nose.undraw()
        for p,c in projections:
            p.undraw()
        disk.undraw()
        disk_x = new_point.getX()
        disk_y = new_point.getY()
    sim_window.getMouse()
    sim_window.close()
main()

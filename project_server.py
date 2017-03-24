import socket
import multiprocessing as mp
import time
import datetime
import cv2
import sys
import numpy as np
import servotest as vc
import maestro as m

MOTOR_NEUTRAL = 1500
ESC_SERVO = 1
STEER_SERVO = 0

ALLOWABLE_OPERATING_CONDITIONS = [
        "startup",
        "normal",
        "autonomous",
        "shutdown",
        "emergency_stop",
]

VERBOSITY = "Debug_Full"

cap = cv2.VideoCapture(0) # get first camera
#cap = None

def messenger():
    pass

def log(string):
    if VERBOSITY == "Debug_Full":
        print string

def warn(string):
    if VERBOSITY in ("Debug_Full", "Debug"):
        print string

def error(string):
    if (VERBOSITY != "Silent"):
        print string

def connection_handler(sock, d, cq, camq):
    client, addr = sock.accept()
    print("Client Connected on {}".format(addr))
    while True:
        client_action = client.recv(3)
        if client_action == "FOO":
            client.sendall(str(datetime.datetime.now()))
            time.sleep(0.1)
	    print "in foo"
        elif client_action == "IMG":
            #frame = d['frame_grab'].copy()
            #gray = frame
	    print "in image part"
            img_str = camq.get()          
            to_expect = str(len(img_str)).zfill(128)
            client.sendall(to_expect)
            if client.recv(4) == "DATA":
                client.sendall(img_str)
		print "in data part"
        elif client_action == "STP":
            client.sendall("HANGUP")
            d["operating_condition"] = "emergency_stop"
            print("Client {} sent STOP signal".format(addr))
            break

        elif client_action == "CTL":
            client.sendall("RDY")
            ctl = client.recv(10)
            cq.put(ctl)
        else:
            break
    client.close()
    print("Client Disconnected")

def driver(d, cq):
    controller = vc.ServoController()
    print "in driver function"  #never enters
    while d["operating_condition"] != "shutdown":
        opcon = d["operating_condition"]
        if opcon == "emergency_stop":
            #vc.serial_control((0,90))
            # TODO While loop to make it keep braking until v = 0
            print("shutting down in three seconds")
            time.sleep(3)
            d["operating_condition"] = "shutdown"
        
        elif opcon == "normal":
            #print("operating")
            control = cq.get()
	    print "control is", control
            #print(control[0:5])
            steering = int(control[0:5])
            throttle = int(control[5::])
            print("the steering is ", steering)
            print("the throttlle is ", throttle)
            controller.setAngle(0, steering)
            controller.setPosition(ESC_SERVO, MOTOR_NEUTRAL + 2*throttle)
            #vc.serial_control(control)
            #print("Applying control {}".format(control))

    if d["operating_conditon"] == "shutdown":
        #vc.serial_control((0,90))
        exit()

def pos_updater(d):
    """
    Position updater: Takes in the vehicle state and consults the sensors
    and positioning system to update.  Alters the position, t_accel (
    tangential acceleration), and a_accel (angular acceleration) vectors in
    the vehicle state.
    """
    while d["operating_condition"] != "shutdown":
        ## TODO: Positioning system and acc/gyro data acquisition
        d["position"] = [0,0,np.pi]
        d["t_accel"] = [0,0,0]
        d["a_accel"] = [0,0,0]

def img_updater(d,q):
    while True: #d["operating_condition"] != "shutdown":
            try:
                ret,frame = cap.read()
                gray = frame#cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                q.put(cv2.imencode('.jpg', gray)[1].tostring())
                time.sleep(1.0/24.0)
                #d['frame_grab'] = gray
            except Exception as e:
                pass
                error("Caught cameraman error {}".format(str(e)))

def emergency_stop(vehicle):
    error("EMERGENCY STOP")
    vehicle["operating_condition"] = "emergency_stop"
    
def set_active(state, target):
    if state:
        state["operating_condition"] = "normal"
        log("Vehicle armed, active")

if __name__ == '__main__':
    vehicle = mp.Manager()
    control_q = mp.Queue()
    client_q = mp.Queue()
    camq = mp.Queue(1)
    vehicle_state = vehicle.dict()
    vehicle_state["operating_condition"] = "startup"
    set_active(vehicle_state, True)

    max_client_connections = 1

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    camera_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if len(sys.argv) == 3:
        ip_addr = sys.argv[1] 
        port = int(sys.argv[2])
    elif len(sys.argv) == 1:
        ip_addr = "localhost"
        port = 8888
    else:
        print("Usage: {} <IP ADDR> <PORT> or no arguments for default"\
                .format(sys.argv[0]))
        exit()
    serversocket.bind((ip_addr,port))
    camera_socket.bind((ip_addr, port+1))
    print("Camera on port {}".format(port+1))
    print("Server running on port {}".format(port))
    serversocket.listen(1)
    
    all_procs = []
    clientelle = [mp.Process(target=connection_handler, args=(serversocket,
        vehicle_state,control_q, camq)) for i\
        in range(max_client_connections)]
    for p in clientelle:
        p.daemon = True
        p.start()
        all_procs.append(p)

    # Start a thread to capture our forward-facing images
    # if cap is not None:
    cameraman = mp.Process(target=img_updater, args=(vehicle_state,camq))
    cameraman.daemon = True
    warn("Booting camera")
    cameraman.start()

    """
    # Start a thread to capture our position 
    magellan = mp.Process(target=pos_updater, args=(vehicle_state,))
    magellan.daemon = True
    warn("Booting navigation system")
    magellan.start()
    """
    # Start the throttle and control interface
    yeager = mp.Process(target=driver, args=(vehicle_state,control_q))
    yeager.daemon = True
    warn("Booting control")
    yeager.start()
    all_procs.append(yeager)

    warn("Vehicle initilization complete")
    serversocket.close()

    while True:
        try:
            pass
            #time.sleep(0.01)
        except KeyboardInterrupt as ki:
            vehicle_state["operating_condition"]="shutdown"
            print("Shutting down system")
            break
    #for proc in all_procs:
    #    proc.join()
    #TODO server robustness - after client disconnect, keep child alive

    print("all processes terminated")

#if cap is not None:
cap.release()
    
exit()

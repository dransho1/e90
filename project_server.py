import socket
import multiprocessing as mp
import time
import datetime
import cv2
import sys
import numpy as np
import vehicle_control as vc

ALLOWABLE_OPERATING_CONDITIONS = [
        "normal",
        "autonomous",
        "shutdown",
        "emergency_stop",
]

VERBOSITY = "Debug_Full"

cap = cv2.VideoCapture(0)
def messenger():
    pass

def log(string):
    if VERBOSITY == "Debug_Full":
        print string

def warn(string):
    if VERBOSITY in ("Debug_Full", "Debug"):
        print string

def error(string):
    if VERBOSITY != "Silent"):
        print string

def connection_handler(sock, d, cq):
    client, addr = sock.accept()
    print("Client Connected on {}".format(addr))
    while True:
        client_action = client.recv(3)
        if client_action == "FOO":
            client.sendall(str(datetime.datetime.now()))
            time.sleep(0.1)
        elif client_action == "IMG":
            frame = d['frame_grab'].copy()
            gray = frame
            img_str = cv2.imencode('.jpg', gray)[1].tostring()
            to_expect = str(len(img_str)).zfill(128)
            client.sendall(to_expect)
            if client.recv(4) == "DATA":
                client.sendall(img_str)

        elif client_action == "STP":
            client.sendall("HANGUP")
            d["operating_condition"] = "emergency_stop"
            print("Client {} sent STOP signal".format(addr))
            break
        else:
            break
    client.close()
    print("Client Disconnected")

def driver(d, cq):
    while d["operating_condition"] != "shutdown":
        opcon = d["operating_condition"]
        if opcon == "emergency_stop":
            #vc.serial_control((0,90))
            # TODO While loop to make it keep braking until v = 0
            print("shutting down in three seconds")
            time.sleep(3)
            d["operating_condition"] = "shutdown"
        
        elif opcon == "normal":
            control = cq.get()
            #vc.serial_control(control)
            print("Applying control {}".format(control))

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

def img_updater(d):
    while d["operating_condition"] != "shutdown":
            try:
                ret,frame = cap.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                d['frame_grab'] = gray
                time.sleep(0.01)
            except:
                pass
                error("Caught cameraman error")

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
    vehicle_state = vehicle.dict()
    set_active(vehicle_state, True)

    max_client_connections = 1

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(len(sys.argv))
    if len(sys.argv) == 3:
        ip_addr = sys.argv[1] 
        port = sys.argv[2]
    elif len(sys.argv) == 1:
        ip_addr = "localhost"
        port = 8888
    else:
        print("Usage: {} <IP ADDR> <PORT> or no arguments for default"\
                .format(sys.argv[0]))
        exit()
    serversocket.bind((ip_addr,port))
    print("Server running on port {}".format(port))
    serversocket.listen(5)
    
    clientelle = [mp.Process(target=connection_handler, args=(serversocket,
        vehicle_state,control_q)) for i\
        in range(max_client_connections_workers)]
    for p in clientelle:
        p.daemon = True
        p.start()

    # Start a thread to capture our forward-facing images
    cameraman = mp.Process(target=img_updater, args=(vehicle_state,))
    cameraman.daemon = True
    warn("Booting camera")
    cameraman.start()

    # Start a thread to capture our position 
    magellan = mp.Process(target=pos_updater, args=(vehicle_state,))
    magellan.daemon = True
    warn("Booting navigation system")
    magellan.start()

    # Start the throttle and control interface
    yeager = mp.Process(target=driver, args=(vehicle_state,control_q))
    yeager.daemon = True
    warn("Booting control")
    yeager.start()

    warn("Vehicle initilization complete")
    serversocket.close()

    while True:

cap.release()
exit()

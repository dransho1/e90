import socket
import multiprocessing as mp
import time
import datetime
import cv2

cap = cv2.VideoCapture(0)
latest_image = None #I know this is horrible practice but meh.
def messenger():
    pass

def connection_handler(sock, d):
    client, addr = sock.accept()
    print("Client Connected on {}".format(addr))
    while True:
        client_action = client.recv(4)
        #print("Recived command {} on {}".format(client_action, addr[0]))
        if client_action == "TIME":
            client.sendall(str(datetime.datetime.now()))
            time.sleep(0.1)
        elif client_action == "IMAG":
            #ret, frame = cap.read()
            frame = d['frame_grab'].copy()
            gray = frame
            img_str = cv2.imencode('.jpg', gray)[1].tostring()
            to_expect = str(len(img_str)).zfill(128)
            client.sendall(to_expect)
            if client.recv(4) == "DATA":
                client.sendall(img_str)
                #time.sleep(0.05)
        elif client_action == "STOP":
            client.sendall("HANGUP")
            print("Client {} sent STOP signal".format(addr))
            break
        else:
            break
    client.close()
    print("Client Disconnected")

if __name__ == '__main__':
    mgr = mp.Manager()
    d = mgr.dict()
    num_workers = 5
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #serversocket.bind(('localhost',8888))
    serversocket.bind(('130.58.194.209',43))
    serversocket.listen(5)
    workers = [mp.Process(target=connection_handler, args=(serversocket,d)) for i in
            range(num_workers)]
    for p in workers:
        p.daemon = True
        p.start()
    while True:
        try:
            ret,frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            d['frame_grab'] = gray
            time.sleep(0.01)
        except:
            print("Server exit on fatal error")
            break
    serversocket.close()
cap.release()
exit()

import socket
import time, sys
import mc

def main():
    controller = mc.hci_init()
    if len(sys.argv) == 3:
        ip_addr = sys.argv[1]
        port = int(sys.argv[2])
    elif len(sys.argv) == 1:
         print("connecting on localhost")
         ip_addr = "localhost"
         port = 8888
    else:
         print("Usage: {} <IP ADDR> <PORT> or no args for default"\
                 .format(sys.argv[0]))
         exit()
                 
    s = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip_addr, port))
    print("Connected")
    i = 0
    while True:#message != "HANGUP":
        try:
            s.send(bytes("CTL", "ASCII"))
            r = s.recv(3)
            if r == bytes("RDY","ASCII"):
                steering, throttle = mc.hci_input(controller)
                steering = str(int(-1*steering*90 + 90)).zfill(5)
                throttle = str(int(-1*90*throttle)).zfill(5)
                #print(throttle)
                #print(steering)
                code = steering+throttle
                s.send(bytes(code,"ASCII"))
        except KeyboardInterrupt:
            s.send("STP")
            break
    print ("Remote end sent HANGUP signal, closing")

main()

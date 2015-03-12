import socket
import cv2
import numpy as np

def recvall(sock, stop):
    chunks = []
    bytes_recd = 0
    data = ""
    while bytes_recd < stop:
        chunk = sock.recv(min((stop-bytes_recd, 2048)))
        if chunk == '':
            raise RuntimeError("No Connection")
        bytes_recd += len(chunk)
        chunks.append(chunk)
    return "".join(chunks)


def main():
    #create an INET, STREAMing socket
    s = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
    #now connect to the web server on port 80
    # - the normal http port
    #s.connect(("localhost", 8888))
    s.connect(("130.58.194.209",43))
    print("Connected")
    chunks = []
    bytes_recd = 0
    message = ""
    while message != "HANGUP":
        try:
            s.send("IMAG")
            image_size = int(recvall(s, 128))
            s.send("DATA")
            message = recvall(s, image_size)
            nparr = np.fromstring(message, np.uint8)
            image = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_GRAYSCALE)
            cv2.imshow('frame', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
               break
        except KeyboardInterrupt:
            s.send("STOP")
    print ("Remote end sent HANGUP signal, closing")
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

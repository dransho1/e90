import socket
#create an INET, STREAMing socket
s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
#now connect to the web server on port 80
# - the normal http port
s.connect(("130.58.194.209", 43))
print("Connected")
chunks = []
bytes_recd = 0
message = ""
while message != "HANGUP":
    try:
        s.send("TIME")
        chunk = s.recv(26)
        if chunk == '':
            raise RuntimeError("socket connection broken")
        chunks.append(chunk)
        bytes_recd = bytes_recd + len(chunk)
        message = chunk
    except KeyboardInterrupt:
        s.send("STOP")
    print message
print ("Remote end sent HANGUP signal, closing")

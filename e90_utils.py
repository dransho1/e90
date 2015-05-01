##########################################################
##  Uitility Files for the E90 Senior Design Project    ##
##  Project by Neil Macfarland and Noah Weinthal        ##
##  Codebase by Noah Weinthal with assistance from      ##
##  Prof. Matthew Zucker.                               ##
##########################################################
def recvall(sock, stop):
"""
Augmented recv ensuring all chunks are recieved and in order
"""
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


class Controller():
    """
    A container for the state-space model for the dynamics of 
    the system.
    """
    state = []
    def __init__(self):
        self.state = []

    def control_for_state(self, x, F_LQR=None):
        if F_LQR:
            return -F_LQR*x
        else:
            F = 
    def system_dynamics(**kwargs):


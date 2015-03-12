##########################################################
##  Uitility Files for the E90 Senior Design Project    ##
##  Project by Neil Macfarland and Noah Weinthal        ##
##  Codebase by Noah Weinthal with assistance from      ##
##  Prof. Matthew Zucker.                               ##
##########################################################

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


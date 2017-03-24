import mc

def main():
    controller = mc.hci_init()
    button =0
    while button==0:
        button = mc.hci_button(controller)            


main()

'''
0 == A
1 == B
'''
# need to get rid of debug statements again
# could setup a publisher for button inputs
# when the button input is 1, kill the car_controller program

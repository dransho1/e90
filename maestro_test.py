#import maestro as m
import servotest as s
import time

def main():

    if 0:
        '''
        controller = m.Controller()
        controller.setTarget(0,8000)
        time.sleep(1.0) # sleep 5 seconds
        controller.setTarget(0,6000)
        time.sleep(1.0)
        controller.close()
        '''
    else:
        controller = s.ServoController()
        controller.setPosition(0, 8000/4)
        time.sleep(1.0)
        controller.setPosition(0, 6000/4)
        time.sleep(1.0)
        controller.closeServo()
    
main()

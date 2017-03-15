#!/usr/bin/env python

import roslib; roslib.load_manifest('joy_test')
import rospy

from std_msgs.msg import Float64


# our controller class
class Controller:

    # called when an object of type Controller is created
    def __init__(self):

        # initialize rospy
        rospy.init_node('car_controller')

        # set up publisher for steering and throttle
        self.servo_steering = rospy.Publisher('/odroid/execution/steering',
                                           Float64)

        self.servo_throttle = rospy.Publisher('/odroid/execution/throttle',
                                           Float64)

        # set up subscriber for joystick data
        rospy.Subscriber('/odroid/commands/steering',
                         Float64, self.str_callback)

        rospy.Subscriber('/odroid/commands/throttle',
                         Float64, self.thr_callback)

    def str_callback(self, st):
        steering = st
        #rospy.loginfo("the steering is ", steering)
        self.servo_steering.publish(steering)
        #controller.setAngle(0, steering)
        #controller.setPosition(ESC_SERVO, MOTOR_NEUTRAL + 2*throttle)

    def thr_callback(self, thr):
        throttle = thr
        #rospy.loginfo("the throttlle is ", throttle)
        self.servo_throttle.publish(throttle)
        #controller.setAngle(0, steering)
        #controller.setPosition(ESC_SERVO, MOTOR_NEUTRAL + 2*throttle)

    def run(self):
        rospy.spin()

    # okay great, now we can send data from one node to another. 
    # want to now use that data to set the angle of the car
    # and integrate this with the car's project_server.py script

# main function
if __name__ == '__main__':
    try:
        ctrl = Controller()
        ctrl.run()
    except rospy.ROSInterruptException:
        pass
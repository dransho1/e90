#!/usr/bin/env python

# Boilerplate initialization stuff -- make sure to load the manifest
# from this package in order to be able to parse all of the correct
# messages. 

import roslib; roslib.load_manifest('joy_test')
import rospy
import mc

# make a message class for reporting
from std_msgs.msg import Float64

#from blobfinder.msg import MultiBlobInfo

######################################################################
# Define a class to implement our node. This gets instantiated once
# when the node is run (see very bottom of file)

class joystick:

    ##################################################################
    # Constructor for our class. Here we initialize any variables
    # which need to be accessed across multiple functions - note that
    # each such member variable is referred to with "self."

    def __init__(self, name):

        # Publish joystick messages to a topic
        self.joystick_steering = rospy.Publisher('/odroid/commands/steering',
                                                    Float64)
        self.joystick_throttle = rospy.Publisher('/odroid/commands/throttle',
                                                    Float64)
        # use float 64 as a message passing

    #################################################################
    # Main loop of program

    def joy_messages(self):
        controller = mc.hci_init()

        while True:
	        steering, throttle = mc.hci_input(controller)
	        steering = int(-1*steering*90 + 90)
	        throttle = int(-1*90*throttle)
	        #rospy.loginfo('steering is ', steering)
	        #rospy.loginfo('throttle is ', throttle)
	        #code = steering+throttle
	        self.joystick_steering.publish(steering)
	        self.joystick_throttle.publish(throttle)
	        rospy.sleep(rospy.Duration(0, 100000)) # just a really short sleep


if __name__ == '__main__':

    rospy.init_node('joystick')
    j = joystick(rospy.get_name())

    try:
        #rospy.spin()
        j.joy_messages()
    except rospy.ROSInterruptException:
        pass

Restart the wifi:
Problem that popped up at the end fo the project. Whenever booted from a cold start, wifi doesn't connect. In reality, it is two Ubuntu wifi services battling with each other, network-manager and networking. To fix, stop both, and restart the network-manager. Should allow you to select networks in the Ubunut MATE desktop interface. If not, try again or reboot via `sudo reboot`:
`sudo service networking stop` --> stop networking 
`sudo service network-manager stop` --> stop network manager 
`sudo service network-manager restart` --> restart network manager 

---------------------------------------------------------

Useful commands:

Shutdown Odroid:
`sudo shutdown -h now`

Start the camera:
`roslaunch openni2_launch openni2.launch`

Viewing data on a host computer with ROS:
`export ROS_MASTER_URI=http://<ip-address>:11311`

Start laserscanner:
`rosrun depthimage_to_laserscan depthimage_to_laserscan image:=/camera/depth/image_raw`  --> runs the laserscan image

Start RViz:
`rosrun rviz rviz`

-------------------------------------------------------

Odroid git push/pull for e90 repo:
	the original e90 git repo "origin" is pointed towards Noah Weinthal's e90 page, which I no longer have access to while using new processor.
	So to write e90 repo, origin = 'myorigin', branch = 'master'
	`git pull myorigin master` --> pull data
	`git push myorigin` --> push data
	...everything else is the same

--------------------------------------------------------
Helpful Unix commands

`df -h` : memory check in MB
`. ~/catkin_ws/devel/setup.bash` : sources the bash to current terminal
`lsmod` : see all the drivers and modules in the system 
`dmesg` : see all things plugged into the computer
`dmesg | grep -i tty` : seaches the dmesg space for the "tty" string
`apt-cache search` : search for online available libs and packages

---------------------------------------------------------
Random issues I resolved:

ROS and python types are different
	"float" vs "Float64"
	Types converted between python and ROS std_msgs

Pygame prints out stuff in terminal
	got rid of issue when the pygame module prints debugging messages to the console
	went into Pygame source code in C
	Commented out the print statement stuff in C, and compiled it from source

Needed to send one message with both steering and throttle:
	Define own ROS message type
	existing message type from ROS
	it's called Int32
		Fixed via custom message, consisting of data types int32 and int32

Prime Sense drivers on the Odroid
1.09 vs 1.08 specs
	1.09 is short range

The joystick works in different directions for different controllers. Flip values on `mc.py` script or `servotest.py` script.

ROS Installation:
	ROS Kinetic on ARM processor: wiki.ros.org/kinetic/Installation/Ubuntu
	(Only package not installed was ros-kinetic-roslz)

Space problem in the odroid? Running out of room after ROS install
	--> ways to save space:
		* delete the .zip files
		* `sudo apt-get clean` --> helps free some space of Ubuntu downloads
		* `sudo apt-get remove <thing to remove>`

------------------------------------------------------

Other less frequent issues:
	The inverter circuit sometimes does not conduct the signal from the Pololu Maestro servo controller. As a result, the Traxxas never connectes to the system, and does that annoying beeping forever. 

	This can be fixed in a hacky way by holding the inverter circuit by its ends and moving it until the beeping stops :/


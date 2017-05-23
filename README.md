# David Ranshous | E90 Engineering Design | Spring 2017

This is my E90 project page. In this README you'll find directions for running the vehicle from scratch. In this **e90/** repo, you'll find scripts for controlling Traxxas vehicle, interfacing with the Pololu servo controller, commanding the vehicle via Pygame and the Logitech gamepad, and reading images into python. The repositories on my main page **/blobfinder** (Zucker 2016), **/joy_test**, **/line_following**, and **cv_test** contain code for running autonomous control, and also exist on the Odroid.

I also included progress reports for each week listed in the **/e90/progress_reports** folder. Those contains quick notes on things to do / things completed each week.

The file **notes.txt** contains useful Unix commands, commands to run the ROS scripts, how to fix wifi issues, and debugging methods for the Odroid processor.

There are a number of ways to use the Traxxas car, including human gamepad control, indoor line following and object avoidance, and outdoor path following. I recommend first getting the car started with a gamepad and Human Control before running any autonomous scripts.

Common trouble: wifi connection with Odroid. The processor has two dueling wifi connectivities, networking and network-manager. Both need to be shutdown and restarted often to initially connect to wifi. See **notes.txt** for instructions.

Also, always ALWAYS run a shutdown command to turn off the processor, otherwise risk destroying the OS. `sudo shutdown -h now` works just fine. This shuts down the OS, so the blue light should go off (indicating OS is shutdown safely), while the amber light remains lit (indicating power to the device).

## Human control (headless)

1. Make sure all batteries are charged. This includes four AA batteries for the Pololu servo controler, the Powerbank for the Odroid, the Logitech controller, and the LiPo batteries for the Traxxas motor. 

2. Connect Powerbank USB charger to the Odroid to start the processor. Wait for Odroid to boot and connect to wifi. 

3. `ssh` into Odroid with IP address. If IP address unknown, connect an HDMI cord to the Odroid, and find out with a display. Open multiple Terminals to control the nodes we will need.

4. Turn on Mamba ESC via switch near the rear of the car, and toggle the Pololu controller on via toggle button near batteries. You will hear a series of chimes and three beeps, followed by a frequent beeping sound. This will continue until the car is successfully connected. 

5. Start the blobfinder node to control the nodes. Run the command `roslaunch blobfinder 

6. Return to your Terminal. Now we will run one ROS node to initialize the gamepad controller for commanding the vehicle.
* First, find the Logitech gamepad and press the center button to turn it on. 
* Next, run the jotstick node, which sends commands from the gamepad via the command `rosrun joy_test joystick.py`.

7. Now we will run the node to control the vehicle. 
* Run the controller node, which receives commands and controls the car via the command `rosrun joy_test car_controller.py`. You should now be able to drive the car around using the gamepad joysticks! Use the Killswitch B button to end the script.

## Line Following and Obejct Avoidance

1. Follow steps 1-6 for the Human Control section to connect to and start the car.

2. Run the ROS node for the camera and laserscanner. 
* Launch the PrimeSense camera with the commmand `roslaunch openni2_launch openni2.launch`. Disregard warning messages.
* Convert the depth image to a laserscan with the command `rosrun depthimage_to_laserscan depthimage_to_laserscan image:=/camera/depth/image_raw`
* (Optional) to see visuals on the vehicle with a computer with ROS installed, run the command `export ROS_MASTER_URI=http://<odroid ip-address>:11311` on the host computer. This allows the host to receive ROS data from the Odroid. Now the host computer can visualize output in Rviz or an image viewer.

3. Run the ROS node for the line following script
* Run the command `rosrun line_following line_follower.py` to start line following. Use the Killswitch B button to end the script.

## Outdoor Path Following

1. Follow steps 1-2 for the Human Control section.

2. Start the Odroid with an HDMI display. Connect the Wifi to the ad-hoc network called *the odroid network*. At the same time, while connecting to it with the Odroid, also connect a host laptop to *the odroid network*. The Odroid and laptop should now be connected to each other.
* Find the IP address of the Odroid on this new network

3. Remove the HDMI display, and follow steps 3-4, and 6 for the Human Control section to connect to, start the car, and initialize gamepad controller (no blobfinder node is necessary in this control).

4. Run the ROS node for the camera only. 
* Launch the PrimeSense camera with the commmand `roslaunch openni2_launch openni2.launch`. Disregard warning messages.

4. Run the ROS node for the path following scripts.
* `cd` to the cv_test scripts directory (`home/catkin_ws/src/cv_test/scripts`)
* Run the command `rosrun cv_test path_follower.py`. This will start the Traxxas for path following outdoors.


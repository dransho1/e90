# David Ranshous | E90 Senior Engineering Design | Spring 2017

This is my E90 project page. These directions are a guide to switching processors on the Traxxas vehicle if/when someone wants to update again. The original system was a Raspberry Pi 2 Model B (2015), which I replaced with an Odroid C2 (2017). 


Here you will find the original scripts for controlling Traxxas vehicle, interfacing with the Pololu servo controller, commanding the vehicle via Pygame and the Logitech gamepad, and reading images into python.

There are also progress reports for each week listed in the **/progress_reports** folder. That contains quick notes on things to do / things completed each week.

The file *notes.txt* contains useful Unix commands, commands to run the ROS scripts, and debugging methods for the Odroid processor.

There are a number of ways to use the Traxxas car, including human gamepad control, indoor line following and obejct avoidance, and outdoor path following. I recommend first getting the car started with a gamepad before running any autonomous scripts.

Common trouble: wifi connection with Odroid. The processor has two dueling wifi connectivities, networking and network-manager. Both need to be shutdown and restarted often to initially connect to wifi. See *notes.txt* for instructions.

Also, always ALWAYS run a shutdown command to turn off the processor, otherwise risk destroying the OS. `sudo shutdown -h` works just fine.

## Human control (headless)

1. Make sure all batteries are charged. This includes four AA batteries for the Pololu servo controler, the Powerbank for the Odroid, the Logitech controller, and the LiPo batteries for the Traxxas motor. 

2. Connect Powerbank USB charger to the Odroid to start the processor. Wait for Odroid to boot and connect to wifi. 

3. ssh into Odroid with IP address. If IP address unknown, connect an HDMI cord to the Odroid, and find out with a display. Open multiple Terminals to control the nodes we will need.

4. Turn on Mamba ESC via switch near the rear of the car, and toggle the Pololu controller on via toggle button near batteries. You will hear a series of chimes and three beeps, followed by a frequent beeping sound. This will continue until the car is successfully connected. 

5. Return to your Terminal. Now we will run one nodes to command the vehicle
* First, find the Logitech and press the center button to turn it on. 
* Next, run the jotstick node, which sends commands from the gamepad via the command `rosrun joy_test joystick.py`.

6. Now we will run the node to control the vehicle. 
* Run the controller node, which receives commands and controls the car via the command `rosrun joy_test car_controller.py`. You should now be ablet o drive the car around!

## Line Following





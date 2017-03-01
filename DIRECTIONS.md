How to operate vehicle and transfer processors on the Traxxas vehicle
-------------------------------------

These directions are a guide to switching processors on the Traxxas vehicle if/when someone wants to update again. The original system was a Raspberry Pi 2 Model B (2015), which I replaced with an Odroid C2 (2017). 

## Turning on the vehicle

1. First things first - try getting the thing on. Connect the Odriod to the battery pack. Make sure the processor and your computer are on the same wifi network. 
   * You can `ssh` into the system if you know the IP address of the processor.
   * If you don't, you can try connecting a display to the processor, and logging in (password provided elsewhere). Once in, run `ifconfig` to see the IP address. Now ssh in from a remote computer


2. Next, run the following command from the Odroid
	```
	python project_server.py <Odroid IP address> <4-digit-port>
	```
	where the arguments include the Odroid's IP address, and a 4 digit port to run on. The default port is 8888. 
	You should see a few printout messages! Good.


3. In a seperte terminal in the client computer, connect a PS3 or Xbox game controller and run:
	```
	python network_controller.py <Odroid IP address> <4-digit-port>
	```
	using the same IP and port from before. You should see some output if you move the controller sticks.


4. Turn on the battery controller by toggle-ing the small button near the battery pack. The servos should mvoe if you move the left stick.


5. Lastly, turn on the ESC. You should hear a series of chimes, followed by a flashing amber light, and finally another series of chimes indicating the connection to the game controller. Congrats, now you can drive it around!
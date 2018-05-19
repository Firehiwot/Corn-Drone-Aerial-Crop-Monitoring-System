
## Software setup for drone

### 1. Mavproxy

Mavproxy is a ground control station (GCS) application for drones and other unmanned aerial vehicles (UAVs). It mainly uses command-line interface unlike other graphic based mission control softwares. Pymavlink allows us to use visual tools for realtime and offline data analysis and plotting

In order to download the mavproxy package we followed the folling steps

1. ```sudo apt-get update    #Update the list of packages in the software center```

2. ```sudo apt-get install screen python-wxgtk2.8 python-matplotlib python-opencv python-pip python-numpy python-dev libxml2-dev libxslt-dev```

Some of these applications were already installed so we chose the ones that aren’t installed. We checked installed applications by using the whereis command to see if they exist in any of the folders on the RPi. 

3. ```sudo pip install future```

The future application allows for easy interfacing between raspberry pi 2 and 3. It allows to convert a python2 or 3 code to a code that is compatible with both. We may not necessarily use this application, but we downloaded it incase if it is necessary at  some point during the project. 

4. ```sudo pip install pymavlink```

5. ```sudo pip install mavproxy```
    
#### Testing Mavproxy
Once the applications were installed, the next step was testing if  the RPi and Pixhawk are able to communicate with each other.As mentioned in the communication setup section first we insured that the serial console is disabled and serial communication via hardware is enabled using raspi-config. We also checked this from the desktop screen by using the top left drop down menu. It is also possible to check that whether or not serial communication is enabled by checking the UART(universal asynchronous receiver-transmitter) value in /boot/config.txt. Check if this value is 1. 

To test the communication we alternated the RX and TX connection between the RPi and Pixhawk and used a common ground for both RPi and Pixhawk. The Pixhawk is already powered with a built-in battery and the RPi was also powered using the micro-usb. It is also possible to use the 5 volt pin on breakout board for the Pixhawk to power the RPi, but we used the micro usb since the power input is more regulated. 

To test the communication we switched to root user and accessed the built-in serial port by using /dev/ttyS0. The --master specified which port (serial/usb/…)
```
sudo -s
mavproxy.py --master=/dev/ttyAMA0 --baudrate 57600 --aircraft MyCopter
```
The baudrate for the communication is set to 57600 because a relatively lower baudrate is more accurate in timing even though it could be slower. 

Running the above test automatically creates a log file in MyCopter folder that keeps track of the flight of the drone. However, in our case the file was empty since we were basically stuck at this step because the communication between the RPi and the Pixhawk was not working. It says that it is “Waiting”. To see if there is at least some connection between the 2, we used the serial5 RX and TX port on the Pixhawk which is mainly used for debugging. The alternate RX and TX connection didn't work, so we switched the two to see how it behaves even though we know that this shouldn’t work. We got a very weird output when the two were connected. This allowed us to confirm that there is connection between the two devices even though we are not getting the desired output. 

We also confirmed that the voltages on the devices were correct ( 3.3 volt for RX/TX pins and 0 volt for ground pin). We used the link command to see if there is connection and it says that there is no link and 0 packets. When the ground pin was accidentally disconnected during measurement; at this point we got a "link OK" output on the screen.  However, when we connected the ground pin back, the link command shows no connection. 

## Communication setup

We used three different approaches to setup communication between the Pixhawk and the RPi. The Pixhawk is the flight controller hardware embedded in the drone that contains ARM processor, sensors, power system control, and communication interfaces such as serial ports, I2C, USB and SPI. 

### Step 1: Turnoff serial console 

Before we started the communication setup, we turned off the serial console in the RPI. The serial console allows us to connect between other computers and the RPi to access the linux console that displays system settings during boot. This is important to check and fix problems during boot or while logging onto the RPi. If this is not turned off it can interfere with the signal that is sent between the RPi and the drone. It is important to note that we only disabled the setting that allows the login shell to be accessible over seria; the serial hardware communication is not disabled. 

The serial console can be turned off in two ways

#### 1. Using raspi-config
    * Type raspi-config in the console
    * Go down to advanced options and hit enter
    * Go down to Serial and hit enter
    * You will be asked the first question below and select No
    * Select Yes for the second question

#### 2. From desktop
From the desktop screen click on the RPi log
***more explanation here***

### Step 2: Setup communication

#### 1. Tx/RX serial communication port

Our first approach was to setup a serial communication between drone and RPi. Since the Pixhawk is inside the drone we used a breakout board to access the pins from outside. 

The TX/RX pins of the RPi were connected to RX/TX pins of the breakout board respectively. This allows us to transmit data between the drone and the RPi. The baud rate ( the rate in which signals are signals are transmitted) the the communication on the RPi should be set to 57600 since the Pixhawk transmits signals at this rate. In addition, it is also important to ensure that there is a common ground between RPi and Pixhawk.

Once the hardware connections are setup correctly, the next step is to test if signals can be transmitted between the two devices.  In order to connect them we used Mavproxy software. The baud rate is set to 57600. The teletypewriter (tty) is USB0. --master specifies which port (serial, USB or network address/port) the UAV is communicating on. --baudrate specifies the baud rate and finally --aircraft specified the directory in which the log files for the drone are created. The Mavproxy software is run as a root user; therefore sudo -s should be used to switch from pi user to root user. 

```
sudo -s 
mavproxy.py --master=/dev/ttyS0 --baudrate 57600 --aircraft MyCopter
```

However this step didn’t work. In fact, we got a console message that the link between the two was “OK” when the common ground pins were disconnected. Otherwise it displays “Waiting for heartbeat” message. Heartbeat is a periodic signal that can be transmitted between devices. Typing “link” on the console once Mavproxy is running can show whether or not the link is ok. 


We are not fully certain as to why the common ground issue gives error. However, at some point, we took apart the entire drone noticed that even though the breakout board is connected directly, the ground pins indicated on the breakout board do not go to the Pixhawk. We alternated between different ground pins and tested the connection, but this didn’t make a difference. Therefore, we switched to using another form of communication. 

#### 2. Universal serial port (USB)
Instead of using the TX/RX pins on the breakout board and RPi, we connected connected a USB port to the RPi and the corresponding power, ground, Data+ (D+) and Data-(D-) pins on the breakout board. We tested the connection using a different tty. However, still the communication didn’t work. There was also a common ground issue in this communication. 

```
mavproxy.py --master=/dev/ttyUSB0 --baudrate 57600
```

#### 3. Direct connection with Pixhawk
    
At this point we decided to take apart the drone and access the Pins directly. When we took it apart, we found out that there is a  microsub pin. Therefore, we planned on setting up a direct micro usb-usb connection between the raspberry pi and the pixhawk. 

Before doing that we installed another ground control station (GCS) software that other people normally use on their laptops to connect with the drone. We installed Mission Planner and APM Planner 2.0 softwares. Both have similar configurations and for later steps during the project we mostly used Mission Planner. 

This software enables us to directly connect the drone with our laptop using a COM (communication) port through the USB. We were able to connect the drone. 


At this point we found out that we had to do software updates and calibrations for the drone before even checking the communication since the drone won’t be able to fly unless clibrations are done properly. Therefore, we took a step back and worked on updating the builtin software in the drone. However, in order test the communication only updates were necessary.  

Click here to see how updates are done for the drone.

Click here to see how we calibrated the drone. 

Once the software is updated , we were also able to connect between the RPi and the drone using the same microsub-usb configuration. 
    
We thought this step would be our final connection method with the drone. However, we found out that this communication only works as long as the drone is turned off since the Pixhawk can be powered from the RPi. This could be a result of the drone preventing double powering of the controller(Pixhawk). One way to avoid this could be stripping the wire that has micro usb and usb  ports on either ends and cutting the power line. However, we decided to move try another alternative that we thought would work after testing the drone in the field. 

#### 4. Sololink wifi

The way we connected with the drone from our laptop during field test was by using the wifi broadcasted from the controller. The drone controller has both radio and wifi signals that can allow it to control the drone over longer distances. In order to do this we used  a UDP connection from mission planner. After having done the field test and encountering the double powering issue of the micro usb usb connection, we decided to test similar form of connection from the RPi using Mavproxy since it is also a GCS software except that it is console based. 

In order to do this we first connected the RPi wifi to the wifi broadcasted from the controller (Sololink) and then accessed the wlan address by typing ifconfig  command from the console. We added this network address in the master command as shown below.  

```
mavproxy.py --master=udp:10.1.1.152:14550 --baudrate 57600 --aircraft MyCopter
``` 

The universal datagram protocol (UDP) is a communication protocol that transfers short data packets called datagrams. This communication worked well for our test. The UDP address can also be modified depending on the wlan address. However, since the RPi will be flying with the drone, the RPi will lose communication with the controller and thus the drone if the drone flies further. The drone is able to communicate with the controller over longer distances since it can use radio communication if the wifi signal is not strong enough. Therefore, it may be necessary to switch to the direct micro usb - usb connection for the actual implementation of the project in the corn field. 

We also tested this communication using Dronekit software which also worked when we used connect command with the right udp (wlan) address. 

```
# Connect to the Vehicle (in this case a UDP endpoint)
vehicle = connect('10.1.1.152:14550', wait_ready=True)
```

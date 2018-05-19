
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
 
 Once the software was installed, we tested the communication between drone and RPi. Click [here](TestingMavproxy.md) for more details. 

### 2. Mission Planner

The mission planner software was installed after we encountered communication issues using the Mavproxy software. This mission planner has features that enabled us to have a better understanding of the calibration system for the drone, simulate drone motion, create a mission for drone flight and locate where the drone is using the gps and compass sensors in the drone. 

After the mission planner is downloaded and connected to the drone using COM port. There are initial setups that need to be done before the flying the drone using this software. 
* [3DR solo firmware update](firmwareupdate.md)
* [Drone Calibration](Calibration.md)





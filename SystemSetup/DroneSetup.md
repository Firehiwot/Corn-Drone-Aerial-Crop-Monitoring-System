## System setup

### Communication setup

We used three different approaches to setup communication between the Pixhawk and the RPi. The Pixhawk is the flight controller hardware embedded in the drone that contains ARM processor, sensors, power system control, and communication interfaces such as serial ports, I2C, USB and SPI. 

### Step 1: Turnoff serial console 

Before we started the communication setup, we turned off the serial console in the RPI. The serial console allows us to connect between other computers and the RPi to access the linux console that displays system settings during boot. This is important to check and fix problems during boot or while logging onto the RPi. If this is not turned off it can interfere with the signal that is sent between the RPi and the drone. It is important to note that we only disabled the setting that allows the login shell to be accessible over seria; the serial hardware communication is not disabled. 

The serial console can be turned off in two ways

1. Using raspi-config
    * Type raspi-config in the console
    * Go down to advanced options and hit enter
    * Go down to Serial and hit enter
    * You will be asked the first question below and select No
    * Select Yes for the second question

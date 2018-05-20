# Python 3.6.4
#
# Based on Cornell_Uni_IMACSS_v9.5-170505.cr1 from Lianhong Gu, ORNL, last revision July 24 2017
# Script by Christine Y. Chang, Cornell University
# Project start date: February 22, 2018
# Last revision: 180320

### Non-native module requirements
# python-seabreeze (https://github.com/ap--/python-seabreeze/, or conda install)
# pyusb (https://github.com/pyusb/pyusb/, or pip install)

### IMACSS Configurations and IMACSSCode convention
# These instruments will be mounted on UAV with fiber optics pointing nadir.
# Communication from RPi to spectrometers are via USB.
# Sample ir/radiance measurements must be matched via timestamp by tower measurements.
#
# Configuration 1: 1 QEPRO only
# IMACSSCODE =
# 0, first outgoing ir/radiance measurement by QEPRO
# 2, if made, dark measurement by QEPRO
# Cycle pattern: 020... if dark measurements are made, otherwise 00...
#
# Configuration 2: 1 FLAME only
# 1, first outgoing ir/radiance measurement by FLAME
# 3, if made, dark measurement by FLAME
# Cycle pattern: 131... if dark measurements are made, otherwise 11...
#
# Configuration 3: 1 QEPRO, 1 FLAME
# 0, first outgoing ir/radiance measurement by FLAME
# 1, outgoing ir/radiance measurement by QEPRO
# 2, if made, dark measurement by FLAME
# 3, if made, dark measurement by QEPRO
# Cycle pattern: 0123... if dark measurements are made, otherwise 0101...

### Operation Sequence
# System should be turned on in following order:
# 1. Turn on RPi, connect computer/phone by VNC
# 2. Start FLAME + QEPRO
# 3. Start python program
#
# System should be turned off in following order:
# 1. Stop program (or switch off raspi)
# 2. Turn off FLAME + QE Pro
import time
import sys
import seabreeze.spectrometers as sb
import usb.core #pyusb module
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import binascii
import os
#from pandas import DataFrame as df

### Classes
class container(object):
	pass

### Constants
# Device IDs set by mfg
flame_vID = 0x2457 #FLAME (any unit)
flame_pID = 0x101e
usb_vID = 0xabcd #Kingston USB drive 64gb (testing; may need to update for other usb drives. find using lsusb)
usb_pID = 0x1234
qepro_vID = 0x2457 #QE Pro (any unit)
qepro_pID = 0x4004

# Directories for saving
homedir = "/home/pi/Documents/FLAME/" #not preferred, better to store on USB given limited space on pi, but if needs must...
usbdir = "/media/pi/046F-990C/"            #use this if available. make sure you have mounted the usb on pi! (mkdir /mnt/usb; sudo mount /dev/sd*1 /mnt/usb) - * can be a or b...

# EP1out commands for FLAME set by Ocean Optics
initialize_device = 0x01
set_integ_time    = 0x02
set_strobe_status = 0x03
set_shutdown_mode = 0x04
query_info        = 0x05 #spectrometer configurations
write_info        = 0x06
request_spectra   = 0x09
set_trigger_mode  = 0x0A
query_nplugins    = 0x0B
query_plugin_ids  = 0x0C
detect_plugins    = 0x0D
led_status        = 0x12
general_i2c_read  = 0x60
general_i2c_write = 0x61
general_spi_io    = 0x62
write_register    = 0x6A
read_register     = 0x6B
read_pcb_temp     = 0x6C
read_irrad_calib  = 0x6D
write_irrad_calib = 0x6E
query_info2       = 0xFE #current operating info

# USB endpoints set by mfg
EP1out = 0x01 #FLAME
EP2in = 0x82  #FLAME, QEPRO
EP6in = 0x86  #FLAME
EP1in = 0x81  #FLAME, QEPRO, USB
EP2out = 0x02 #USB, QEPRO

#FLAME constants
F = container()
F.npx = 2048
F.StartIntegTimeInuSec = 100000         #starting integration time is 100ms (same as OceanView first guess). Can lower if needed.
F.MaxIntegTimeInuSec = int(6.5e7)       #65 seconds. instrument absolute max is 65.535 seconds
F.MinIntegTimeInuSec = 1000              #1 msec is instrument minimum
F.MaxSatLevel = 28000                   #tested saturation level for FLAME1. the manual says 0x55F0 (22000) but this is not correct
F.SpecPeakMax = int(0.9*F.MaxSatLevel)    # 90% max
F.SpecPeakMin = int(0.75* F.MaxSatLevel)  # 75% max
F.dummy = 0                             #average of dummy pixels !!! may need to change this later if local parameters are wiped

#QEPRO constants
Q = container()
Q.npx = 1044
Q.StartIntegTimeInuSec = 1000000        #starting guess for integration time is 1s
Q.MaxIntegTimeInuSec = 10*60*1000000    #10 min. QEPro absolute max is 60 min
Q.MinIntegTimeInuSec = 8000             #8 msec. instrument will time out below 1ms!
Q.MaxSatLevel = 200000                  #Saturation level for QEPro
Q.SpecPeakMax = int(0.9*Q.MaxSatLevel)    # 90% max
Q.SpecPeakMin = int(0.75* Q.MaxSatLevel)  # 75% max
Q.dummy = 1554.0                        #average of dummy pixels

#Other constants
interval = 30                        #in seconds. duration to read when activated
guess_interval = 10
guess_period = time.time()
guess_end = guess_period + guess_interval
flag = 0
c = 0
IntegTimeArray = [0]
### Functions

def get_device(vendorId, productId, name):
	"""Get USB device configuration and show to user:
	Resets the device in case it was not released on previous program run.
	Returns device for interfacing throughout program."""
	device = usb.core.find(idVendor = vendorId, idProduct = productId) 
	if device is None:
		print("Warning: %s not found!" % name)
	else:
		device.reset()
		cfg = device.get_active_configuration()
		#print(cfg) #uncomment this to see the device config
	return device



def get_spec_cfg():
	"""Get spectrometer configuration variables as stored by Ocean Optics:
	See cfg_headers for contents. Returns config for records."""
	cfg_idx = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C,0x0D, 0x0E, 0x0F, 0x10]
	cfg_headers = ["SerialNo", "WL0", "WL1", "WL2", "WL3", "Straylightconst", "NL0", "NL1", "NL2", "NL3", "NL4", "NL5", "NL6", "NL7", "NLpoly", "Opticalbenchconfig", "Flameconfig"]
	global flame
	print("Spectrometer configuration: \n")
	config = []
	for i in cfg_idx:
		flame.write(EP1out, [query_info, i])
		msg = flame.read(EP1in, 16, 100) #always reads 16 bytes. wait 100ms for response.
		config.append(''.join(map(chr,msg[2:]))) #read only the relevant parts of the message
		print(cfg_headers[i], ": ", config[i])
	return config
	
def get_spec_info():
	"""Gets spectrometer information as stored by Ocean Optics:
	See info_headers for contents. Returns number of packets and USB comm speed."""
	
	print("\nSpectrometer settings: \n")
        
	flame.write(EP1out, [read_pcb_temp, 0x00])
	msg = flame.read(EP1in, 16, 100)
	print('TEMP:' + str(msg)) 
	msg1 = (msg[2],msg[1])
	print('after lsb msb shift' + str(msg1))
	msg1 = binascii.hexlify(bytearray(msg1))
	msg1= int(str(msg1), 16)
	print('decimal conv' + str(msg1))
	TEMP = 0.003906*msg1

	return TEMP
##
##def initialize_dataframe(spectra):
##	headers = ["Timestamp", "IntegTimeInuSec"] + spectra[0].tolist()
##	dataframe = pd.DataFrame(columns = headers)
##	return dataframe
    


# PROGRAM START



flame = get_device(flame_vID, flame_pID, "FLAME")
qepro = get_device(qepro_vID, qepro_pID, "QEPRO")
usb_drive = get_device(usb_vID, usb_pID, "USB")



###TEMP DATA###
#flame.write(EP1out, [initialize_device, 0x00]) #initialize spectrometer
#config = get_spec_cfg() #get serial number to store later in output
 #check initial spec info
#print(msg)
c=0	


fintegtime = F.StartIntegTimeInuSec
qintegtime = Q.StartIntegTimeInuSec

#status = input("\nPress Enter to acquire spectra or another key to exit.\n")
#print (status)
flame_name = "FLAME_spectra_{}.csv".format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
flame_nameTransposed = "FLAME_spectra1_{}.csv".format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
qepro_name = "QEPRO_spectra_{}.csv".format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
meta_name = "meta_{}.csv".format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
start_time = time.time()
period = time.time()

period_end = period + interval

def temperature():

    TEMP = get_spec_info()
    print(str(TEMP))
    if flame != None:
            flame.reset()
            usb.util.dispose_resources(flame) # release flame
    if qepro != None:
            usb.util.dispose_resources(qepro) # release qepro
    if usb_drive != None:
            usb.util.dispose_resources(usb_drive) # release usb
    return TEMP





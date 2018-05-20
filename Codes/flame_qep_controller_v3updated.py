# Python 3.6.4
#
# Based on Cornell_Uni_IMACSS_v9.5-170505.cr1 from Lianhong Gu, ORNL, last revision July 24 2017
# Script by Christine Y. Chang, Rahul Desai, Shinjini Biswas and Firehiwot Gurara Cornell University
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
#import flame_control as control
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

def plot_spectra(spectra, title_, px_range):
	"""simple plot of spectra stored for visual comparison"""
	plt.plot(spectra[0][px_range[0]: px_range[1]], spectra[1][px_range[0]: px_range[1]])
	plt.ylabel("Counts")
	plt.xlabel("Pixels")
	plt.title(title_)
	plt.savefig(savedir+"figures/" + title_ + ".jpg")
	#plt.show() # to use this in terminal, make sure you do "xhost +" to enable access to xwindow
	plt.gcf().clear() #prevent bleeding to next plot

def optimize_loop(spec, spectra, integtime, ts):
	if spec.model == "QE-PRO":
		S=Q
		spectype = "QEPRO"
		px_range = [10, 1034]
	elif spec.model == "USB2000PLUS":
		S=F
		spectype = "FLAME"
		px_range = [20, 2048]
	
	plot_spectra(spectra, (spectype + "_Initial_spectra"), px_range)
	SpecPeakCurr = max(spectra[1][px_range[0]:px_range[1]])
	
	if SpecPeakCurr < S.SpecPeakMin or SpecPeakCurr > S.SpecPeakMax:
		integtime, spectra, ts = optimize_integtime(spec, integtime, SpecPeakCurr, S, px_range)
		SpecPeakCurr = max(spectra[1][px_range[0]:px_range[1]])
		
	print("Optimized integration time: %d usec" % integtime)
	print("Optimized SpecPeak: %d counts" % SpecPeakCurr)
	plot_spectra(spectra, (spectype + "_Optimized_spectra"), px_range)
	return integtime, spectra, ts

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
	


def optimize_integtime(spec, start_time, SpecPeak, S, px_range):

	""" Optimize integration time, adapted from IMACSS v9.5
	"""
	n = 1
	SpecPeak0 = SpecPeak #store initial value
	Integtime0 = float(start_time) #store initial value
	print("Peak", str(SpecPeak0), "/", str(start_time), "usec out of bounds. Optimization starting...")
	
	#Initial adjustment
	if SpecPeak > S.MaxSatLevel-1: # Peak pixel was likely saturated; need large reduction in linear time
		CurrIntegTimeInuSec = int(start_time * 0.5) 
	else:
		CurrIntegTimeInuSec = int(start_time * (0.85*S.MaxSatLevel) / SpecPeak - S.dummy) #18700 is 85% of max; dummy offset does not depend on integration time
	
	CurrIntegTimeInuSec = timecheck(CurrIntegTimeInuSec, S)
	
	SpecPeak, spectra, ts = guess(CurrIntegTimeInuSec, n, spec, px_range)
	
	#Continue optimization if the first attempt was insufficient
	while SpecPeak < S.SpecPeakMin or SpecPeak > S.SpecPeakMax: #or 
		guess_period=time.time()
		if guess_period < guess_end:
			if SpecPeak < 1:
				SpecPeak = 1 
			li = 0
			if abs(SpecPeak - SpecPeak0) < 0.05*S.MaxSatLevel or abs(SpecPeak - SpecPeak0) > 0.25*S.MaxSatLevel: #if change in peak is not enough or too much?
				li = 1
			if (CurrIntegTimeInuSec - Integtime0) * (SpecPeak - SpecPeak0) < 0: #if one overshot the other?
				li = 1
			if SpecPeak0 >= S.MaxSatLevel-10 or SpecPeak >= S.MaxSatLevel-10:       #if specpeak is still too large
				li = 1
			if (abs(CurrIntegTimeInuSec - Integtime0)/Integtime0) > 0.5:        #if change in time is >50%
				li = 1
			if li == 0:
				term = Integtime0 + (CurrIntegTimeInuSec - Integtime0) * ((0.85*S.MaxSatLevel) -SpecPeak0) / (SpecPeak - SpecPeak0)
				Integtime0 = float(CurrIntegTimeInuSec)
				CurrentIntegTimeInuSec = int(1.0+term)
			else:
				Integtime0 = CurrIntegTimeInuSec
				if SpecPeak < (S.MaxSatLevel - 100) :
					CurrIntegTimeInuSec = 1 + int(CurrIntegTimeInuSec * (0.85*S.MaxSatLevel)  / SpecPeak)
				else:
					CurrIntegTimeInuSec = 1 + int(CurrIntegTimeInuSec * (0.5*S.MaxSatLevel) / SpecPeak)
			
			CurrIntegTimeInuSec = timecheck(CurrIntegTimeInuSec, S)
			
			n += 1
			SpecPeak, spectra, ts = guess(CurrIntegTimeInuSec, n, spec, px_range)
			print("Storing timestamp: %s" % ts)
#			guess_period=time.time()
			print('check for 10 seconds, time elapsed is ' + str(guess_end - guess_period))
		else:
			print('10 seconds elapsed, Timeout')
			global flag
			flag = 1
			break
#		print(time.time())
#		global T
#		T = T-1
#		if (time.time() > T + 10):
#			print('##################################################')
#			break
	print('exiting optim integ time')
	
	return CurrIntegTimeInuSec, spectra, ts
##
##def initialize_dataframe(spectra):
##	headers = ["Timestamp", "IntegTimeInuSec"] + spectra[0].tolist()
##	dataframe = pd.DataFrame(columns = headers)
##	return dataframe
    
def save_spectra(dataframe, spectra, ts, csv_name,integtime,ftemp):
	"""need to save timestamp, integration time, and spectra"""
	#dataframe = dataframe.assign(TEMP=TEMP)

        dataframe = dataframe.assign(Temperature=ftemp)
        dataframe = dataframe.assign(integration_time=integtime)
	dataframe = dataframe.assign(pixels=spectra[0])
	dataframe[ts] = spectra[1]
	Plotname = savedir + "data/" + csv_name
	print(Plotname)
	with open((Plotname), 'w') as f:
		dataframe.to_csv(f, index=False, na_rep = "NaN")
	return dataframe
    
#with integration time and transposed
##def save_spectra(dataframe, integtime, spectra, ts, csv_name):
##	"""need to save timestamp, integration time, and spectra"""
##	#df = pd.Datarame(integtime)
##	global c
##	
##	#dataframe["Pixel Wavelength"] = spectra[0]
##	#print ("############!@#$%^&*" + str(integtime))
##	#dataframe = dataframe.assign(rahul=spectra[0])
##	
##	#dataframe[ts] = spectra[1]
##	#dataframe.insert integtime
##	
##	dataframe.loc[c] = [ts, integtime] + spectra[1].tolist() #rewriting the timestamps
##	dataframe = dataframe.append(dataframe.loc[c])
##	print ("ccccccccccccccccccccccccccccc =" + str(c))
##	#dataframe.append(df)
##	Plotname = savedir + "data/" + csv_name
##	print(Plotname)
##	with open((Plotname), 'w') as f:
##		dataframe.to_csv(f, index=False, na_rep = "NaN")
##		
##	
##	return dataframe
##
    
def timecheck(time_, S):
	"""Make sure time is within our set boundaries."""
	if time_ > S.MaxIntegTimeInuSec:
		time_ = S.MaxIntegTimeInuSec
	elif time_ < S.MinIntegTimeInuSec:
		time_ = S.MinIntegTimeInuSec 
	return time_
	
def guess(integtime, n, spec, px_range):
	"""Test guesses within the integration time optimization loop."""
	print("===========\nGuess %d" % n)
	print("Integration time: %d usec" % integtime)
	spectra, ts = acquire_spectra(spec, integtime)
	SpecPeak = max(spectra[1][px_range[0]:px_range[1]])
	print("SpecPeak: %d counts" % SpecPeak)
	return SpecPeak, spectra, ts

def acquire_spectra(spec, integtime):
	"""Send integration time and acquire one new spectrum."""
	spec.integration_time_micros(integtime)
	#time.sleep(1/1000) #wait 1msec for settings to update
	spectra = spec.spectrum()
	ts = str(datetime.datetime.now()).split('.')[0] #get timestamp of spectrum
	return spectra, ts
##def updatecsv(csvname):
##	
##	dataframe = pd.read_csv(str(csvname))
##	#dataframe= dataframe.convert_objects(convert_numeric=True)
##	dataframe = dataframe.insert(0, 'integration Time', IntegTimeArray[0:])
##	dataframe = dataframe.to_csv(csvname)

###
# PROGRAM START

#qdata = pd.DataFrame()
fdata = pd.DataFrame()
metadata = pd.DataFrame()

##flame = get_device(flame_vID, flame_pID, "FLAME")
##print("DEVICE: $$$$$$$"+str(flame))
##qepro = get_device(qepro_vID, qepro_pID, "QEPRO")
usb_drive = get_device(usb_vID, usb_pID, "USB")

if usb_drive != None:
	savedir = usbdir
else:
	savedir = homedir
	
### Detect spectrometers
devices = sb.list_devices()

if len(devices) < 1 or len(devices) > 2:
	sys.exit("1 or 2 spectrometers must be connected.\n")


def find_spec():
    for i in range(len(devices)):
            temp = sb.Spectrometer(devices[i])
            print("DEVICE NAME IS @@@@@@@@@@@@@" + str(temp))
            if temp.model == "USB2000PLUS":
                    fspec = temp
                    #usb.util.dispose_resources(devices[i])
            elif temp.model == "QE-PRO":
                    qspec = temp


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
name =savedir + "data/" + flame_name
nameTransposed = savedir + "data/" + flame_nameTransposed

start_time = time.time()


for i in range(len(devices)):
        temp = sb.Spectrometer(devices[i])
        print("DEVICE NAME IS @@@@@@@@@@@@@" + str(temp))
        if temp.model == "USB2000PLUS":
                fspec = temp
                #usb.util.dispose_resources(devices[i])
        elif temp.model == "QE-PRO":
                qspec = temp

def measure():

    global fintegtime
    global flame_name
    global fdata
    global fspec
    global name
    global nameTransposed
##    flame_name = "FLAME_spectra_{}.csv".format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
##    print(flame_name)
##    flame_nameTransposed = "FLAME_spectra1_{}.csv".format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
##    qepro_name = "QEPRO_spectra_{}.csv".format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
##    meta_name = "meta_{}.csv".format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

    print("Entered callback")
    period = time.time()
    period_end = period + interval
    while True:
    #	if status != "":
    #		break
                    c=0
                    print("Starting collection...")
                    
                    while period < period_end:
                                    print('Time now is' + str(period))
                                    # 1. set integration time and retrieve spectra with initial guess
                                    #    QE Pro always goes first because it takes longer and we want to minimize difference between FLAME and QEPRO
    ##                    if qepro != None:
    ##                            qspectra, qts = acquire_spectra(qspec, qintegtime)	
    ##                            print("First Q timestamp: %s" % qts)
    ##                    if flame != None:
                                    fspectra, fts = acquire_spectra(fspec, fintegtime)
                                    print("First F timestamp: %s" % fts)
                                    
                                    # 3. Optimize integration time for QE Pro then FLAME.
    ##                    if qepro != None:
    ##                            qintegtime, qspectra, qts = optimize_loop(qspec, qspectra, qintegtime, qts)
    ##                            
    ##                    if flame != None:
                                    fintegtime, fspectra, fts = optimize_loop(fspec, fspectra, fintegtime, fts)
                                                    
                                    # 4. Save optimized measurements.
    ##                            if qepro != None:
    ##                                    qdata = initialize_dataframe(qspectra)
    ##                                    qdata = save_spectra(qdata, qspectra, qts, qepro_name)
                                    #if flame != None:
                                    print('saving spectra data')
                                    print(fspectra[1])
    #				fdata = initialize_dataframe(fspectra)
    ##				IntegTimeArray.append(fintegtime)
                                            #fspec.close()
                                            #ftemp= control.temperature()
                                    ftemp=0 #DUMMY VALUE. REMOVE THIS
                                            #print(i)
                                            #print(devices[i])
                                            #fspec = sb.Spectrometer(devices[i])
                                            #fspec._open_device(devices[i])
                                    fdata = save_spectra(fdata, fspectra, fts, flame_name,fintegtime,ftemp)
    #				c=c+1
                        #            else:
                         #                           break
                                    #metadata = save_configs() #what do we want to put in here?
                                    period = time.time()
                    
    #	status = input("Press Enter to acquire spectra or another key to exit.\n")
    #	period = time.time()
    #	period_end = period + (interval) #repeat for interval
                    print(time.time())
                    break
    ##
    ##    if flame != None:
    ##            usb.util.dispose_resources(flame) # release flame
    ##    if qepro != None:
    ##            usb.util.dispose_resources(qepro) # release qepro
    ##    if usb_drive != None:
    ##            usb.util.dispose_resources(usb_drive) # release usb

    #print(IntegTimeArray)

    


    #pd.read_csv(str(name)).T.to_csv(str(nameTransposed),header=False)


#measure()
print("Signing you off, Shepard.")
# PROGRAM END


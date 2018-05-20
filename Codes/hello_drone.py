# Script by Christine Y. Chang, Rahul Desai, Shinjini Biswas and Firehiwot Gurara Cornell University
# adapted from : http://python.dronekit.io/guide/taking_off.html
print ("Start code for drone motion")
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import sys , random , time
from pymavlink import mavutil

#drone = connect("udp:10.1.1.152:14550",wait_ready=True) #WIFI connection to pi
drone = connect("/dev/ttyACM0", wait_ready=True) #direct USB connection to pi. Make sure this is connected after the drone is already powered on!

battery_threshold=40

print("Initial setting check for drone")
print("GPS:"+ str(drone.gps_0))
print("Battery level:" + str(drone.battery.level))
print ("Is Armable?:" + str(drone.is_armable))
print("System status:" +str(drone.system_status.state))
print("Mode:" + str(drone.mode.name)) # gives information about flight mode: guided, loiter, autonomous...
print ("Altitude:" + str(drone.attitude)) # gives pitch, yaw and roll values
print ("Velocity:" + str(drone.velocity))
print ("Global Location:" + str(drone.location.global_frame))
print ("Global Location-Relative Altitude" + str(drone.location.global_relative_frame))
print ("Local Location" +   str(drone.location.local_frame))
print ("Groundspeed:" + str(drone.groundspeed))
print ("Airspeed:" + str(drone.airspeed))

# absolute gps coordinates
home_abs_lat = drone.location.global_frame.lat
home_abs_long = drone.location.global_frame.lon

# relative gps coordinates
home_rel_lat = drone.location.global_relative_frame.lat
home_rel_long = drone.location.global_relative_frame.lon

print ("Lat_abs = " + str(home_abs_lat))
print ("Lat_rel = " + str(home_rel_lat))
print ("Long_abs= " + str(home_abs_long))
print ("Long_rel= " + str(home_rel_long))


# exit if battery status is too low
if (drone.battery.level)<= battery_threshold:
    print ("Battery is low: can't start flight")
    sys.exit()
##    
##while (drone.is_armable==False):
##    print ("Waiting for drone to be armed")
##    time.sleep(1)
##    
##drone.mode=VehicleMode("GUIDED")
##drone.armed=True
##
##while not drone.armed:
##    print ("Waiting for arming")
##    time.sleep(1)

# download and clear previous commands in the drone
cmds = drone.commands
cmds.download()
cmds.wait_ready() # wait until download is complete
cmds.clear()

lat_min=42.724113
lat_max=42.724155

long_min= -76.651047
long_max= -76.651367

latitude=random.uniform(lat_min, lat_max)
longitude=random.uniform(long_min, long_max)

#mav_util_nav_waypoint: navigate to specified position
# mav_frame_global_relative: sets altitude as relative to home position( home_position=0)
num_of_waypoints = 3

waypoint = []

# create home waypoint
waypoint.append(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, 0))

for n in range (1,num_of_waypoints+1):
    waypoint.append(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, 1))
    #waypoint.append(waypoint(n))
    cmds.add(waypoint[n])

for cmd in waypoint:
    cmds.add(cmd)
    print(cmd)
    
#for n in range (0,num_of_waypoints):
 #   print(cmds.waypoint[n])

drone.close()

print("done")










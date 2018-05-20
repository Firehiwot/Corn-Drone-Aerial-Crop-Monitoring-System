#!/usr/bin/python
# adapted from : http://python.dronekit.io/guide/taking_off.html
print ("Start code for drone motion")
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import sys , random , time
from pymavlink import mavutil
import math
#import flame_qep_controller_v4 as spec

drone = connect("udp:10.1.1.152:14550",wait_ready=True)
battery_threshold=20

# intial setting check
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

print ("Lat = " + str(home_abs_lat))
print ("Lat = " + str(home_rel_lat))


##distance from waypoints##
def get_distance_meters(loc1, loc2):
    
    lat1=  math.radians(loc1.lat)
    lat2 = math.radians(loc2.lat)
    long1 = math.radians(loc1.lon)
    long2= math.radians(loc2.lon)
    R= 6373
    dlat = lat2 - lat1
    dlong = long2 - long1
    
    a = (math.sin(dlat/2))**2 + math.cos(lat1)*math.cos(lat2)* (math.sin(dlong/2))**2
    c= 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    distance = R*c
    return distance/1000

def distance_to_waypoint(nxt):
    nxt = drone.commands.next
    if nxt == 0:
        return 0 # home
    item = drone.commands[nxt]
    lat = item.x
    long = item.y
    alt = item.z
    targetwaypointlocation = LocationGlobalRelative(lat,long,alt)
    print ("AT___________"+ str(drone.location.global_frame))
    distance = get_distance_meters(drone.location.global_frame, targetwaypointlocation)
    return distance

# exit if battery status is too low
if (drone.battery.level)<= battery_threshold:
    print ("Battery is low: can't start flight")
    sys.exit()
##    


# download and clear previous commands in the drone
cmds = drone.commands
cmds.download()
cmds.wait_ready() # wait until download is complete
cmds.clear()

# preset gps locaitons for drone

h_lat=42.4487249
h_long=-76.4769787
latA=42.4486451
latB=42.4481181
longA=-76.4772559
longB=-76.4752182
drone.airspeed =0.5
drone.groundspeed=0
# create way points
#mav_util_nav_waypoint: navigate to specified position
# mav_frame_global_relative: sets altitude as relative to home position( home_position=0)
num_of_waypoints = 4

waypoint = []
# create home waypoint
waypoint.append(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0,0,  h_lat, h_long,0))
waypoint.append(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0,0, 0,0, latA, longA, 0))
waypoint.append(Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,mavutil.mavlink.MAV_CMD_NAV_LOITER_TIME,0,0,10,0,0,0,latA,longA,0))
waypoint.append(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0,0, 0, 0, h_lat, h_longB, 0))
#waypoint.append(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0, 0, 0, 0, 0, 0, h_lat, h_long,1))

for cmd in waypoint:
    cmds.add(cmd)
    print(cmd)

cmds.upload()

###Checks if configuration is correct for the drone to be armed###
##while (drone.is_armable==False):
##    print ("Waiting for drone to be armed")
##    time.sleep(1)
    
drone.mode=VehicleMode("STABILIZE")
drone.armed=True

##Checks if drone was successfully armed##
#while not drone.armed:
 #   print ("Waiting for arming")
  #  time.sleep(1)
    
#drone.simple_takeoff(0)
drone.mode=VehicleMode("AUTO")
print(drone.commands.next)
time.sleep(20)
print(drone.commands.next)
time.sleep(20)
print(drone.commands.next)
time.sleep(20)
print(drone.commands.next)
time.sleep(20)
print(drone.commands.next)
N=0
drone.close()
while N==1:
    print(drone.airspeed)
    nextwaypoint = drone.commands.next
    print ("Waypoint nowwwwwwwwwwwwwww " + str (nextwaypoint))
    if (nextwaypoint == num_of_waypoints):
        break
    elif(nextwaypoint>0 and nextwaypoint <= num_of_waypoints):
        print("inside" + str(nextwaypoint))
        distance = distance_to_waypoint(nextwaypoint)
        print("distance" + str (distance))
        if (distance <= 1):
            print("point" +str (nextwaypoint)+ "reached")         
#drone.close()
print("done")




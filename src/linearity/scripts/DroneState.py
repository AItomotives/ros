#!/usr/bin/env python

import rospy, json
from collections import deque
from mavros_msgs.msg import Param, GPSRAW
from sensor_msgs.msg import BatteryState
from geometry_msgs.msg import TwistStamped, PoseStamped
from std_msgs.msg import String
from linearity.srv import DroneData

class DroneState:

    def __init__(self):
        self.time_interval = 0.5
        self.curr_time = 0
        self.state_list = deque()
        self.statesTracked = 0
        self.wind_speed = 0
        self.wind_angle = 0
        self.battery_voltage = 0
        self.battery_current = 0
        self.position_x = 0
        self.position_y = 0
        self.position_z = 0
        self.orientation_x = 0
        self.orientation_y = 0
        self.orientation_z = 0
        self.orientation_w = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.velocity_z = 0
        self.angular_x = 0
        self.angular_y = 0
        self.angular_z = 0
        self.linear_acceleration_x = 0
        self.linear_acceleration_y = 0
        self.linear_acceleration_z = 0

    def updateStateList(self):
        if self.statesTracked < 200:
            self.state_list.append(self.droneSnapshot())
        else:
            self.state_list.popleft()
            self.state_list.append(self.droneSnapshot())


    def droneSnapshot(self):
        
        return {
            "time": self.curr_time,
            "wind_speed": self.wind_speed,
            "wind_angle": self.wind_angle,
            "battery_voltage": self.battery_voltage,
            "battery_current": self.battery_current,
            "position_x": self.position_x,
            "position_y": self.position_y,
            "position_z": self.position_z,
            "orientation_x": self.orientation_x,
            "orientation_y": self.orientation_y,
            "orientation_z": self.orientation_z,
            "orientation_w": self.orientation_w,
            "velocity_x": self.velocity_x,
            "velocity_y": self.velocity_y,
            "velocity_z": self.velocity_z,
            "angular_x": self.angular_x,
            "angular_y": self.angular_y,
            "angular_z": self.angular_z,
            "linear_acceleration_x": self.linear_acceleration_x,
            "linear_acceleration_y": self.linear_acceleration_y,
            "linear_acceleration_z": self.linear_acceleration_z
        }

def updateDroneState(message, ds):
    
    if isinstance(message, GPSRAW):
        print(message)
    elif isinstance(message, BatteryState):
        ds.battery_voltage = message.voltage
        ds.battery_current = message.current
    elif isinstance(message, TwistStamped):
        ds.velocity_x = round(message.twist.linear.x, 4)
        ds.velocity_y = round(message.twist.linear.y, 4)
        ds.velocity_z = round(message.twist.linear.z, 4)
        ds.angular_x = round(message.twist.angular.x, 4)
        ds.angular_y = round(message.twist.angular.y, 4)
        ds.angular_z = round(message.twist.angular.z, 4)
    elif isinstance(message, PoseStamped):
        ds.position_x = round(message.pose.position.x, 6)
        ds.position_y = round(message.pose.position.y, 6)
        ds.position_z = round(message.pose.position.z, 6)
        ds.orientation_w = round(message.pose.orientation.w, 6)
        ds.orientation_x = round(message.pose.orientation.x, 6)
        ds.orientation_y = round(message.pose.orientation.y, 6)
        ds.orientation_z = round(message.pose.orientation.z, 6)
    elif isinstance(message, String) or message == "datapls":
        #gonna publish to a new topic here
        print ds.droneSnapshot()

    else:
        print("not doing stuff")

def getDroneState(message):
    global ds
    return json.dumps(list(ds.state_list))

def spinfunc(ds):
    rospy.init_node('DroneStateNode', anonymous=True)
    r = rospy.Rate(1/ds.time_interval)
    #This is possible to use but its raw gps data and harder to work with
    #rospy.Subscriber("mavros/gpsstatus/gps1/raw", GPSRAW, updateDroneState)
    rospy.Subscriber("mavros/battery", BatteryState, updateDroneState, ds)
    rospy.Subscriber("mavros/local_position/velocity_local", TwistStamped, updateDroneState, ds)
    rospy.Subscriber("mavros/local_position/pose", PoseStamped, updateDroneState, ds)
    s = rospy.Service('linearity/get_data', DroneData, getDroneState)
    # pub = rospy.Publisher('linearity/data', String, queue_size=100)

    while not rospy.is_shutdown():
        # pub.publish()
        ds.curr_time += ds.time_interval
        ds.updateStateList()
        r.sleep()  



if __name__ == '__main__':
    global ds
    ds = DroneState()
    ds.state_list.append(ds.droneSnapshot())
    spinfunc(ds)
    print(ds.droneSnapshot())
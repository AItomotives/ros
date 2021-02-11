#!/usr/bin/env python

import rospy
import mavros
import random
from linearity.msg import GoToWaypoint
from mavros_msgs.msg import WaypointList, Waypoint



def callback(data):
    global remainingWaypoints
    global missionFinished
    if len(remainingWaypoints) == 0 and not missionFinished:
        for waypoint in data.waypoints:
            #if waypoint.command == goto
                # check for a score
                    # make an atomic
            # if waypoint.command == rtl
                # check for land 
                    # make an atomic
            #else
            remainingWaypoints.append(waypoint)
    elif missionFinished:
        rospy.loginfo("We finished the mission")
    else:
        nextWaypointIndex = random.randrange(len(remainingWaypoints))

        nextWaypoint = remainingWaypoints[nextWaypointIndex]
        remainingWaypoints.pop(nextWaypointIndex)
        rospy.loginfo("next waypoint is a " + str(nextWaypoint.command) + "command. It has coordinates X: %s, Y: %s, Z: %s", nextWaypoint.x_lat, nextWaypoint.y_long, nextWaypoint.z_alt)
            
        pub = rospy.Publisher('decide_waypoint', GoToWaypoint, queue_size=10)

        pub.publish(nextWaypointIndex)


            # rospy.loginfo(rospy.get_caller_id() + "Waypoint number" + str(i) + " is X: %s, Y: %s, Z: %s", waypoint.x_lat, waypoint.y_long, waypoint.z_alt)
            # if waypoint.is_current:
            #     rospy.loginfo("========== Going to do ^this^ one now ==========")
            # i += 1
        rospy.loginfo("")

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('ainav', anonymous=True)

    rospy.Subscriber("mavros/mission/waypoints", WaypointList, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    global remainingWaypoints
    remainingWaypoints = []
    global missionFinished 
    missionFinished = False
    listener()
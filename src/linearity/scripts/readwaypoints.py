#!/usr/bin/env python

import rospy
import mavros
import random
from linearity.msg import GoToWaypoint
from mavros_msgs.msg import WaypointList, Waypoint

from WPWrapper import WPWrapper
from WaypointManager import WaypointManager
from RandomStrategy import RandomStrategy 
from SmartStrategy import SmartStrategy
from WPWrapper import WPWrapper


def callback(data):
    global needToBuild
    global waypointManager
    global curwaypoint
    if needToBuild:
        waypointManager.load_new_mission(data.waypoints)
        needToBuild = False

    print("curwaypoint: ", curwaypoint, "data.current_seq: ", data.current_seq)
    if curwaypoint == data.current_seq:
        rospy.loginfo("waiting to do")
    else:
        nextWaypointWrapped = waypointManager.getNextWaypoint()
        if (nextWaypointWrapped == "Mission Complete"):
            print("Ladies and gentlemen, we gottem")
        else:
            nextWpPos = nextWaypointWrapped.positionInList
            rospy.loginfo("curwaypoint is set to " + str(nextWpPos) + " and current_seq is set to " + str(data.current_seq))
            
            if nextWaypointWrapped == "Mission Complete":
                #do some stuff instead bc we finished the mission
                return
            
            nextWaypoint = nextWaypointWrapped.waypoint
            rospy.loginfo("next waypoint is a " + str(nextWaypoint.command) + " command. It has coordinates X: %s, Y: %s, Z: %s", nextWaypoint.x_lat, nextWaypoint.y_long, nextWaypoint.z_alt)

            if (data.current_seq != 1):
                pub = rospy.Publisher('decide_waypoint', GoToWaypoint, queue_size=10)

            pub.publish(nextWpPos)
            curwaypoint = nextWpPos

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
    global needToBuild
    needToBuild = True
    global waypointManager
    waypointManager = WaypointManager(SmartStrategy())
    global curwaypoint
    curwaypoint = 1
    listener()
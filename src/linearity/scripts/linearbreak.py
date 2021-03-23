#!/usr/bin/env python

import rospy
import mavros
from linearity.msg import GoToWaypoint
from mavros_msgs.msg import WaypointList, Waypoint
from mavros_msgs.srv import WaypointSetCurrent

def change_current_waypoint(new_waypoint_msg):
    new_waypoint = new_waypoint_msg.waypointNum
    rospy.loginfo("setting new waypoint to" + str(new_waypoint))
    rospy.wait_for_service('/mavros/mission/set_current')
    rospy.loginfo("setting new waypoint to" + str(new_waypoint))
    try:
        waypoint_set_current = rospy.ServiceProxy('/mavros/mission/set_current', WaypointSetCurrent)
        resp1 = waypoint_set_current(new_waypoint)
        rospy.loginfo(resp1)
    except rospy.ServiceException as e:
        rospy.logerr(e)

def listener():
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("decide_waypoint", GoToWaypoint, change_current_waypoint)

    rospy.spin()

if __name__ == '__main__':
    listener()
from ros.src.linearity.scripts import WPWrapper, DroneState
import math


class UtilityStrategy:

    path = '\\\\wsl$\\Ubuntu-18.04\\home\\bgood12\\exact\\build\\rnn_examples\\evaluate_rnn'
    genome = 'C:\\Users\\rasca\\Downloads\\rnn_genome_1994.bin'

    def _calcDistance(self, waypoint, dronestate: DroneState):
        data = dronestate.getdata()
        # currentX = data[-1].get("position_x")
        # currentY = data[-1].get("position_y")
        # currentZ = data[-1].get("position_z")
        # todo delete these once the above works
        currentX = DroneState.DroneState.position_x
        currentY = DroneState.DroneState.position_y
        currentZ = DroneState.DroneState.position_z
        # Calculate distance between the two points
        return math.sqrt(math.pow(waypoint.x_lat - currentX, 2) + math.pow(waypoint.y_long - currentY, 2) + math.pow(waypoint.z_alt - currentZ, 2))


    def getWaypointCosts(self, waypoint, dronestate: DroneState):
        distance = self._calcDistance(waypoint, dronestate)
        batteryLossRate = self.getBatteryCurrent(dronestate)

        return batteryLossRate * distance * -1 # The -1 gives us a positive cost because current is negative when discharging, which is always

    def getBatteryCurrent(self, dronestate: DroneState):
        data = dronestate.getdata()
        return data[-1].get("battery_current")


    def getReturnWaypoint(waypoints):
        # searches in the list of waypoints for the waypoint detailing a return to home, and returns it
        for atomic_waypoint in waypoints:
            for WPWapper in atomic_waypoint.waypoints:
                if WPWrapper.CommandID == 21:
                    return atomic_waypoint

    def getNext(self, waypoints, visited, dronestate: DroneState):
        home_wp = self.getReturnWaypoint(waypoints)
        home_cost = self.getWaypointCosts(home_wp, dronestate)

        # default choice is to go home, and default utility is the cost of going home without attaining a reward
        next_utility = 0 - home_cost
        next_wp = home_wp

        for atomic_waypoint in waypoints:
            if atomic_waypoint not in visited:
                wp_cost = self.getWaypointCosts(atomic_waypoint, dronestate)
                wp_reward = atomic_waypoint.getRewardValue()
                wp_utility = wp_reward - wp_cost

                if wp_utility > next_utility:
                    next_wp = atomic_waypoint
                    next_utility = wp_utility

        print("waypoint was chosen and it is worth", next_utility, "points")
        return next_wp
              
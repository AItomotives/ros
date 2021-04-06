from ros.src.linearity.scripts import WPWrapper, DroneState
import math
import predict


class UtilityStrategy:

    path = '\\\\wsl$\\Ubuntu-18.04\\home\\bgood12\\exact\\build\\rnn_examples\\evaluate_rnn'
    genome = 'C:\\Users\\rasca\\Downloads\\rnn_genome_1994.bin'

    def _calcDistance(self, waypoint, data):
        currentX = data[-1].get("position_x")
        currentY = data[-1].get("position_y")
        currentZ = data[-1].get("position_z")
        # todo delete these once the above works
        currentX = DroneState.DroneState.position_x
        currentY = DroneState.DroneState.position_y
        currentZ = DroneState.DroneState.position_z
        # Calculate distance between the two points
        return math.sqrt(math.pow(waypoint.x_lat - currentX, 2) + math.pow(waypoint.y_long - currentY, 2) + math.pow(waypoint.z_alt - currentZ, 2))


    def getWaypointCosts(self, waypoint, dronestate: DroneState):
        data = dronestate.getdata()
        distance = self._calcDistance(waypoint, data)
        batteryStuff = predict(self.path, self.genome, data)

        return batteryStuff / distance

    def getBatteryCurrent(self, data):
        return data[-1].get("battery_current")


    def getReturnWaypoint(waypoints):
        # searches in the list of waypoints for the waypoint detailing a return to home, and returns it
        for atomic_waypoint in waypoints:
            for WPWapper in atomic_waypoint.waypoints:
                if WPWrapper.CommandID == 21:
                    return atomic_waypoint

    def getNext(self, waypoints, visited, dronestate: DroneState):
        next_wp = None
        next_utility = -100
        if visited.len() = 0:

            for atomic_waypoint in waypoints:
                if atomic_waypoint != self.getReturnWaypoint(waypoints):
                    wp_reward = atomic_waypoint.getRewardValue()
                    wp_dist = self._calcDistance(atomic_waypoint, dronestate.getdata())

                    wp_utility = wp_reward / wp_dist

                    if wp_utility > next_utility:
                        next_wp = atomic_waypoint
                        next_utility = wp_utility
            
            print("waypoint was chosen and it is worth", next_utility, "points")
            return next_wp

        else:
            home_wp = self.getReturnWaypoint(waypoints)
            home_cost = self.getWaypointCosts(home_wp, dronestate)

            next_wp = home_wp
            next_utility = home_wp.getRewardValue() - home_cost

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
              
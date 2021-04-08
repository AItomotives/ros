from WPWrapper import WPWrapper
import math
from predict import predict


class UtilityStrategy:

    counter = 0

    def _calcDistance(self, waypoint, data):
        currentX = data.get("position_x")
        currentY = data.get("position_y")
        currentZ = data.get("position_z")
        # Calculate distance between the two points
        print("_calcdistance waypoint is: ", waypoint)
        waypoint = waypoint.waypoints[0].waypoint
        return math.sqrt(math.pow(waypoint.x_lat - currentX, 2) + math.pow(waypoint.y_long - currentY, 2) + math.pow(waypoint.z_alt - currentZ, 2))


    def getWaypointCosts(self, waypoint, dronestate):
        distance = self._calcDistance(waypoint, dronestate[-1])
        batteryStuff = predict(dronestate, self.counter)
        self.counter += 1

        return batteryStuff / distance

    def getBatteryCurrent(self, data):
        return data[-1].get("battery_current")


    def getReturnWaypoint(self, waypoints):
        # searches in the list of waypoints for the waypoint detailing a return to home, and returns it
        for atomic_waypoint in waypoints:
            for WPWapper in atomic_waypoint.waypoints:
                if WPWapper.commandID == 20:
                    return atomic_waypoint

    def getNext(self, waypoints, visited, dronestate):
        next_wp = None
        next_utility = -100
        if len(visited) == 0:

            for atomic_waypoint in waypoints:
                if atomic_waypoint != self.getReturnWaypoint(waypoints):
                    wp_reward = atomic_waypoint.getRewardValue()
                    wp_dist = self._calcDistance(atomic_waypoint, dronestate[-1])

                    wp_utility = wp_reward / wp_dist

                    if wp_utility > next_utility:
                        next_wp = atomic_waypoint
                        next_utility = wp_utility

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
              
from WPWrapper import WPWrapper
import math
from predict import predict


class UtilityStrategy:

    counter = 0
    # drone_range = 1215 #Meters
    drone_range = 15000

    def _calcDistance(self, waypoint, data):
        currentX = float(data.get("position_x"))
        currentY = float(data.get("position_y"))
        currentZ = float(data.get("position_z"))
        # Calculate distance between the two points
        print("_calcdistance waypoint is: ", waypoint)
        wp = waypoint.waypoints[0].waypoint
        return math.sqrt(math.pow(wp.x_lat - currentX, 2) + math.pow(wp.y_long - currentY, 2) + math.pow(wp.z_alt - currentZ, 2))


    def getWaypointCosts(self, waypoint, dronestate):

        self.counter += 1
        predictions = predict(dronestate, self.counter)
        distance = float(self._calcDistance(waypoint, predictions))
        if distance < self.drone_range:
            cost = distance * math.e**(1/(-1*(distance-self.drone_range))) + distance
        else:
            cost = float("inf")
        return cost,distance


    def getBatteryCurrent(self, data):
        return data[-1].get("battery_current")


    def getReturnWaypoint(self, waypoints):
        # searches in the list of waypoints for the waypoint detailing a return to home, and returns it
        for atomic_waypoint in waypoints:
            for WPWapper in atomic_waypoint.waypoints:
                if WPWapper.commandID == 20:
                    return atomic_waypoint

    def getNext(self, waypoints, visited, dronestate):
        home_wp = self.getReturnWaypoint(waypoints)
        home_cost = self.getWaypointCosts(home_wp, dronestate)
        next_wp = home_wp
        next_utility = home_wp.getRewardValue() - home_cost[0]
        chosen_dist = 0
        wp_reward = 0

        for atomic_waypoint in waypoints:
            if atomic_waypoint not in visited:
                wp_cost_distance = self.getWaypointCosts(atomic_waypoint, dronestate)
                wp_reward = atomic_waypoint.getRewardValue()
                wp_utility = wp_reward - wp_cost_distance[0]
                if wp_utility > next_utility:
                    next_wp = atomic_waypoint
                    next_utility = wp_utility
                    chosen_dist = wp_cost_distance[1]

        print("###############################################")
        print("Reward: ", wp_reward)
        print("Utility: ", next_utility)
        print("Distance: ", wp_cost_distance)
        self.drone_range -= chosen_dist
        return next_wp

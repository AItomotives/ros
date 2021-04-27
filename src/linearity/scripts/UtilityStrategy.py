from WPWrapper import WPWrapper
import math
from predict import predict

LOOKAHEAD_DEPTH = 1

class UtilityStrategy:

    counter = 0
    drone_range = 2430 #Meters
    homeWP = None


    def _calcDistance(self, waypoint, data):
        currentX = float(data.get("position_x"))
        currentY = float(data.get("position_y"))
        currentZ = float(data.get("position_z"))
        # Calculate distance between the two points
        print("_calcdistance waypoint is: ", waypoint)
        wp = waypoint.waypoints[0].waypoint
        return math.sqrt(math.pow(wp.x_lat - currentX, 2) + math.pow(wp.y_long - currentY, 2) + math.pow(wp.z_alt - currentZ, 2))

    def calcWPDistanceToHome(self,waypoint):
        home_wp = self.getHomeCoordinates()
        homeX = home_wp[0]
        homeY = home_wp[1]
        homeZ = home_wp[2]
        wp = waypoint.waypoints[0].waypoint
        return math.sqrt(math.pow(wp.x_lat - homeX, 2) + math.pow(wp.y_long - homeY, 2) + math.pow(wp.z_alt - homeZ, 2))

    def getWaypointCosts(self, waypoint, dronestate):

        self.counter += 1
        predictions = predict(dronestate, self.counter)
        distance = float(self._calcDistance(waypoint, predictions))

        if distance > self.drone_range:
            cost = float("inf")
        elif self.calcWPDistanceToHome(waypoint) > self.drone_range - distance:
            cost = float("inf")
        else: cost = distance * math.e**(1/(-1*(distance-self.drone_range))) + distance

        # if distance < self.drone_range:
        #     cost = distance * math.e**(1/(-1*(distance-self.drone_range))) + distance
        # else:
        #     cost = float("inf")
        return cost,distance


    def getBatteryCurrent(self, data):
        return data[-1].get("battery_current")


    def getReturnWaypoint(self, waypoints):
        # searches in the list of waypoints for the waypoint detailing a return to home, and returns it
        for atomic_waypoint in waypoints:
            for WPWapper in atomic_waypoint.waypoints:
                if WPWapper.commandID == 20:
                    self.homeWP = atomic_waypoint
                    return atomic_waypoint

    def getHomeCoordinates(self):
        home_wp = self.homeWP
        x = home_wp.waypoints[0].waypoint.x_lat
        y = home_wp.waypoints[0].waypoint.y_long
        z = home_wp.waypoints[0].waypoint.z_alt
        return x,y,z

    def calcUtility(self, atomic_waypoint, waypoints, visited, dronestate, depth=0):
        home_wp = self.homeWP
        home_cost = self.getWaypointCosts(home_wp, dronestate)
        
        chosen_dist = 0

        wp_cost_distance = self.getWaypointCosts(atomic_waypoint, dronestate)
        wp_reward = atomic_waypoint.getRewardValue()
        single_wp_utility = wp_reward - wp_cost_distance[0]

        total_utility = single_wp_utility

        if depth < LOOKAHEAD_DEPTH and atomic_waypoint is not home_wp:
            for atomic_waypoint_lookahead in waypoints:
                if not atomic_waypoint_lookahead == atomic_waypoint and atomic_waypoint_lookahead not in visited:
                    lookahead_utility = self.calcUtility(atomic_waypoint_lookahead, waypoints, visited, dronestate, depth+1)
                    if single_wp_utility + lookahead_utility > total_utility:
                        total_utility = single_wp_utility + lookahead_utility
        return total_utility

    def getNext(self, waypoints, visited, dronestate):

        self.homeWP = self.getReturnWaypoint(waypoints)

        home_wp = self.homeWP
        home_cost = self.getWaypointCosts(home_wp, dronestate)
        next_wp = home_wp
        next_utility = home_wp.getRewardValue() - home_cost[0]
        chosen_dist = 0

        for atomic_waypoint in waypoints:
            if atomic_waypoint not in visited:
                wputility = calcUtility(atomic_waypoint, waypoints, visited, dronestate)
                if wp_utility > next_utility:
                    next_wp = atomic_waypoint
                    next_utility = wp_utility
                    chosen_dist = wp_cost_distance[1]
                    print("Reward: ", wp_reward)
                    print("Utility: ", wp_utility)
                    print("Distance: ", wp_cost_distance)

        print("waypoint was chosen and it is worth", next_utility, "points")
        self.drone_range -= chosen_dist
        return next_wp

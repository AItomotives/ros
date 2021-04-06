class UtilityStrategy:

    self.waypointCosts = {} # key-value pair for atomic waypoint objects & their associated costs

    def initWaypointCosts():
        # TODO. gets costs associated with each atomic waypoint
        pass

    def getBatteryCurrent():
        # TODO. gets current current in battery
        pass

    def getReturnWaypoint(waypoints):
        # searches in the list of waypoints for the waypoint detailing a return to home, and returns it
        for atomic_waypoint in waypoints:
            for WPWapper in atomic_waypoint.waypoints:
                if WPWrapper.CommandID == 21:
                    return atomic_waypoint

    def getNext(self, waypoints, visited):
        home_wp = getReturnWaypoint(waypoints)
        home_cost = self.waypointCosts[home_wp]  

        # default choice is to go home, and default utility is the cost of going home without attaining a reward
        next_utility = 0 - home_cost
        next_wp = home_wp

        for atomic_waypoint in waypoints:
            if atomic_waypoint not in visited:
                wp_cost = self.waypointCosts[atomic_waypoint]
                wp_reward = atomic_waypoint.getRewardValue()
                wp_utility = wp_reward - wp_cost

                if wp_utility > next_utility:
                    next_wp = atomic_waypoint
                    next_utility = wp_utility

        print("waypoint was chosen and it is worth", next_utility, "points")
        return next_wp
              
class SmartStrategy:

    def getNext(self, waypoints, visited):
        maxreward = -100
        next_wp = None
        for atomic_waypoint in waypoints:
            if atomic_waypoint not in visited:
                reward = atomic_waypoint.getRewardValue() 
                if reward > maxreward:
                    maxreward = reward
                    next_wp = atomic_waypoint
        
        print("waypoint was chosen and it is worth", maxreward, "points")
        return next_wp
            


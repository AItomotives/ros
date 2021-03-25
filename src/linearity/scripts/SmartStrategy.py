class SmartStrategy:

    def getNext(self, waypoints, visited):
        max = 0
        next_wp = None
        for atomic_waypoint in waypoints:
            if atomic_waypoint not in visited:
                reward = atomic_waypoint.getRewardValue() 
                if reward > max:
                    max = reward
                    next_wp = atomic_waypoint
            


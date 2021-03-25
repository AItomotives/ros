import mavros

class AtomicWaypoints:

    def __init__(self, waypoints):
        if waypoints:
            self.waypoints = []
            for waypoint in waypoints:
                self.waypoints.append(waypoint)
        else:
            self.waypoints = []
        self.curwaypoint = 0

    def addWaypoint(self, waypoint):
        self.waypoints.append(waypoint)

    def getNextWaypoint(self):
        print("Atomic: getting next waypoint")
        print("currentwaypoint is now", self.curwaypoint)
        retval = self.waypoints[self.curwaypoint]
        self.curwaypoint +=1
        return retval
    
    def isCompleted(self):
        return self.curwaypoint >= len(self.waypoints)

    def getRewardValue():
        total = 0
        for wp in self.waypoints:
            total += wp.rewardvalue
        return total
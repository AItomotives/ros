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
        self.curwaypoint += 1
        return self.waypoints[self.curwaypoint-1]
    
    def isCompleted(self):
        return self.curwaypoint == len(self.waypoints)
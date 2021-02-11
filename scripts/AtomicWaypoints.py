import mavros

class AtomicWaypoints:

    def __init__(self, waypoints)
        self.waypoints - waypoints
        self.curwaypoint = 0

    def getNextWaypoint():
        self.curwaypoint += 1
        return self.waypoints[self.curwaypoint-1]
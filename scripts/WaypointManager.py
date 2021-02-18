from mavros_msgs.msg import Waypoint, WaypointList

class WaypointManager:

    def __init__(self, nextWaypointStrategy):
        self.waypoints = []
        self.visited = []
        self.listOfCommandsWithRewards = [16]
        self.nextWaypointStrategy = nextWaypointStrategy
        self.currentAtomic = None

    def load_new_mission(self, waypointList):
        self.waypoints = []
        self.visited = []
        self.currentAtomic = None
        i = 0
        while i < len(waypointList.waypoints):
            waypoint = waypointList.waypoints[i]
            if waypoint.id == 26: # rewards
                pass
            elif waypoint.id == 21: #land?
                pass
            atomic = AtomicWaypoint() #make atomic remember the original number
            atomic.addwaypont(waypoint)
            if waypoint.id == 19: #return to home?
                if waypointList.waypoints[i+2] == 21: #?land?
                    atomic.addwaypoint(waypointList.waypoints[i+1])
                    atomic.addwaypoint(waypointList.waypoints[i+2])
                    atomic.addwaypoint(waypointList.waypoints[i+3])
                else:
                    atomic.addwaypoint(waypointList.waypoints[i+1])
            elif waypoint.id in self.listOfCommandsWithRewards: # goto?
                atomic.addwaypoint(waypointList.waypoints[i+1])
            self.waypoints.append(atomic)

    def getNextWaypoint(self):
        if self.currentAtomic:
            wp = self.currentAtomic.getNextWaypoint()
            if self.currentAtomic.isCompleted():
                self.currentAtomic = None
            return wp
        elif not self.visited:
            self.currentAtomic = self.waypoints[0]
            return self.getNextWaypoint
        elif len(self.visited) == len(self.waypoints):
            return "Mission Complete"
        else:
            #This is where the logic can go
            #Just set self.currentAtomic to something not in visited
            #and return self.getNextWaypoint
            self.currentAtomic = self.nextWaypointStrategy.getNext(self.waypoints, self.visited)
            return self.getNextWaypoint
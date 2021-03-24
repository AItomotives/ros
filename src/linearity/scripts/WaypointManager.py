from mavros_msgs.msg import Waypoint, WaypointList

from WPWrapper import WPWrapper
from AtomicWaypoints import AtomicWaypoints

class WaypointManager:

    def __init__(self, nextWaypointStrategy):
        self.waypoints = []
        self.visited = []
        self.listOfCommandsWithRewards = [16,20]
        self.nextWaypointStrategy = nextWaypointStrategy
        self.currentAtomic = None

    # TODO Revisit this logic
    def load_new_mission(self, waypointList):
        # Nuke old waypoints, we're on a new mission, partner.
        self.waypoints = []
        self.visited = []
        self.currentAtomic = None
        for i in range(0, len(waypointList)):
            waypoint = waypointList[i]
            # If the command is not a reward, a landing command, or a delay, it's a waypoint.
            if waypoint.command != 26 and waypoint.command != 21 and waypoint.command != 93:
                atomic = AtomicWaypoints([]) # Make atomic remember the original number
                wrappedWP = WPWrapper(waypoint,i)
                atomic.addWaypoint(wrappedWP)
                if waypoint.command in self.listOfCommandsWithRewards: # goto?
                    wrappedWP.setReward(waypointList[i+1].param1)
                if waypoint.command == 19: #return to home?
                    if waypointList.waypoints[i+2] == 21: #?land?
                        landwp = WPWrapper(waypointList[i+2], i+2)
                        landwp.setReward(waypointList[i+3].param1)
                        atomic.addWaypoint(landwp)
                self.waypoints.append(atomic)

    def getNextWaypoint(self):
        if self.currentAtomic:
            wp = self.currentAtomic.getNextWaypoint()
            if self.currentAtomic.isCompleted():
                self.currentAtomic = None
            return wp
        elif not self.visited:
            self.currentAtomic = self.waypoints[0]
            return self.getNextWaypoint()
        elif len(self.visited) == len(self.waypoints):
            return "Mission Complete"
        else:
            #This is where the logic can go
            #Just set self.currentAtomic to something not in visited
            #and return self.getNextWaypoint
            self.currentAtomic = self.nextWaypointStrategy.getNext(self.waypoints, self.visited)
            return self.getNextWaypoint()
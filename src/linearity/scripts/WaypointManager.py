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
            # print("When building we find waypoints in the order of", i, waypoint)
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
        print("we finished building the waypoints. currently there are " + str(len(self.waypoints)) + "waypoints")

    def getNextWaypoint(self):
        print("getting next waypoint")
        if self.currentAtomic:
            print("has an atomic")
            wp = self.currentAtomic.getNextWaypoint()
            print("we got a next waypoint from the atomic. its command #", wp.positionInList)
            if self.currentAtomic.isCompleted():
                print("Is complete")
                self.visited.append(self.currentAtomic)
                self.currentAtomic = None
            return wp
        elif not self.visited:
            print("There is no visited so we set the current thing were doing to the takeoff")
            self.currentAtomic = self.waypoints[0]
            return self.getNextWaypoint()
        elif len(self.visited) == len(self.waypoints):
            print("Mission Complete")
            return "Mission Complete"
        else:
            #This is where the logic can go
            #Just set self.currentAtomic to something not in visited
            #and return self.getNextWaypoint
            print("calling the strategy to get us a next atomic")
            self.currentAtomic = self.nextWaypointStrategy.getNext(self.waypoints, self.visited)
            return self.getNextWaypoint()
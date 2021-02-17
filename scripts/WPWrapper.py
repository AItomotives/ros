
class WPWrapper:

    def __init__(self, waypoint, positionInList):
        self.waypoint = waypoint
        self.positionInList = positionInList
        self.commandID = waypoint.command
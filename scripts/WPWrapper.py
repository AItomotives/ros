
class WPWrapper:

    def __init__(self, waypoint, positionInList):
        self.waypoint = waypoint
        self.positionInList = positionInList
        self.commandID = waypoint.command
        self.rewardvalue = 0

    def setReward(self, reward):
        self.rewardvalue = reward
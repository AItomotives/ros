
class WPWrapper:

    def __init__(self, waypoint, positionInList):
        self.waypoint = waypoint
        self.positionInList = positionInList
        self.commandID = waypoint.command
        self.rewardvalue = 0

    # TODO Setter not necessary here, maybe refactor, or don't I'm not your dad
    def setReward(self, reward):
        self.rewardvalue = reward
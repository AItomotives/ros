import random

class RandomStrategy:

    def getNext(self, waypoints, visited):
        nextwp = None
        while not nextwp:
            test = random.choice(waypoints)
            if test not in visited:
                nextwp = test
        return nextwp
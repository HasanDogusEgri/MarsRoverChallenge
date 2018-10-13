
import threading
from time import sleep
from Globals import *


class Rover:
    # In order not to get an error while initialization, there must be one whitespace between the variables while entering.
    def __init__(self):
        self.moving = False
        while True:
            try:
                self.xCoordinate, self.yCoordinate, self.face = input("\nEnter the initial coordinates of the rover: ").split(' ')
                self.xCoordinate = int(self.xCoordinate)
                self.yCoordinate = int(self.yCoordinate)

                if self.xCoordinate > 0 and self.xCoordinate < 6 and self.yCoordinate > 0 and self.yCoordinate < 6:
                    pass
                else:
                    raise ValueError

                if self.face is not "S" and self.face is not "W"\
                    and self.face is not "E" and self.face is not "N":
                    raise ValueError
                break
            except ValueError:
                prRed(" Enter the initial rover coordinates in correct format.\n"+
                      "  For example: 1 3 S")


    def getCoordinates(self):
        return self.xCoordinate, self.yCoordinate, self.face


    #This method creates a thread for collecting samples that are assigned to the rover.
    def createThread(self, route):
        movementThread = threading.Thread(target=self.goToDestination,args=(route,))
        movementThread.start()


    def moveToL(self):
        self.face = DIRECTIONS[(DIRECTIONS.index(self.face) - 1)]


    def moveToR(self):
        self.face = DIRECTIONS[(DIRECTIONS.index(self.face) + 1)]


    def moveToM(self):
        getattr(self, "moveTo%s" % self.face)()
        sleep(1)


    def moveToN(self):
        if self.yCoordinate < PLATEAUYMAX:
            self.yCoordinate = (self.yCoordinate + 1)


    def moveToS(self):
        if self.yCoordinate > 1:
            self.yCoordinate = (self.yCoordinate - 1)


    def moveToE(self):
        if self.xCoordinate < PLATEAUXMAX:
            self.xCoordinate = (self.xCoordinate + 1)


    def moveToW(self):
        if self.xCoordinate > 1:
            self.xCoordinate = (self.xCoordinate - 1)


    def isMoving(self):
        return self.moving


    def goToDestination(self, route):
        self.moving = True
        for step in range(len(route)):
            getattr(self, "moveTo%s" % route[step])()
        self.moving = False
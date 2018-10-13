
from random import *

"""
    Only thing that is done by mars class is dynamic function call according to the rovers' status.
    (In the dynamic function call, 0 is used for 'not in use', 1 is used for 'in use'.For instance,
    createMessage01 is for assigning missions to the first rover.)
    If none of them is in use, then 00 coded function is called.In this function, a random selection is made.
    If one of them is in use, then 01 or 10 coded function is called to assign mission to the specific rover. 
    If both of them are in use, then 11 coded function is called.This function sends a stream starting with 0 to satellite.
    This means there is no rover available.    
"""
class MarsBase:
    #99 is for initialization of self.choice variable.It can be any value but integer.
    def __init__(self):
        self.choice = 99


    def createMessage(self, moving1, moving2, rover1, rover2):
        return getattr(self, "createMessage{0}{1}".format(int(moving1), int(moving2)))(rover1, rover2)


    def createMessage00(self, rover1, rover2):
        self.choice = randint(1,2)
        if self.choice == 1:
            xCoordinate, yCoordinate, face = rover1.getCoordinates()
        else:
            xCoordinate, yCoordinate, face = rover2.getCoordinates()
        message = ("1" + str(xCoordinate) + str(yCoordinate) + face) + str(self.choice)
        return message


    def createMessage01(self, rover1, rover2):
        self.choice=1
        xCoordinate, yCoordinate, face = rover1.getCoordinates()
        message = ("1" + str(xCoordinate) + str(yCoordinate) + face) + str(self.choice)
        return message


    def createMessage10(self, rover1, rover2):
        self.choice=2
        xCoordinate, yCoordinate, face = rover2.getCoordinates()
        message = ("1" + str(xCoordinate) + str(yCoordinate) + face) + str(self.choice)
        return message


    def createMessage11(self, rover1, rover2):
        xCoordinate, yCoordinate, face, self.choice = 0, 0, 'W', 3
        message = ("0" + str(xCoordinate) + str(yCoordinate) + str(face) + str(self.choice))
        return message

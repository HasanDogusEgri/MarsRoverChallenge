
from MarsBase import MarsBase
import socket
from Rover import Rover
import threading

messageToSend = routeByteLength = route = ""


def startMarsBaseProcess():
    marsBaseProcessThread = threading.Thread(target = MarsBaseProcessThread())
    marsBaseProcessThread.start()


def sendMapCoordinates(rover1, rover2, mapSocket):
    x1, y1, f1 = rover1.getCoordinates()
    x2, y2, f2 = rover2.getCoordinates()
    mapCoordinates = str(x1) + str(y1) + str(f1) + str(x2) + str(y2) + str(f2)
    mapSocket.send(mapCoordinates.encode())


def sendRoversInfo(marsBase, rover1, rover2, marsSocket):
    global messageToSend
    messageToSend = marsBase.createMessage(rover1.isMoving(), rover2.isMoving(), rover1, rover2)
    marsSocket.send(messageToSend.encode())


def determineAvailability():
    global messageToSend
    if int(messageToSend[0]) == int(1):
        return True
    else:
        return False


def getRouteLength(socket):
    # routeByteLength is needed for mars socket to know how many bytes that will be read.
    # If routeByteLength starts with 0, then the length of route that will be sent is going to have
    # one digit. Otherwise, two digits.
    global routeByteLength
    routeByteLength = getMessageViaSocket(2, socket)

    # Returns true if the routeByteLength has two digits. False otherwise.
    if int(routeByteLength[0]) == int(0):
        return int(routeByteLength[-1])
    else:
        return int(routeByteLength)


def receiveRoute(socket):
    global route
    route = getMessageViaSocket(getRouteLength(socket), socket)


def assignRouteToRover(rover1, rover2):
    # If the chosen rover is rover1 then execute the if block. Otherwise, execute else block.
    if int(messageToSend[-1]) == int(1):
        rover1.createThread(route)
    else:
        rover2.createThread(route)


def getMessageViaSocket(bufferSize, socket):
    return socket.recv(bufferSize).decode()


def MarsBaseProcessThread():
    #Initialization of the base on Mars and rovers.
    marsBase = MarsBase()
    rover1 = Rover()
    rover2 = Rover()


    # Opening the socket for communication with the satellite.
    marsBaseSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    marsBaseSocket.bind((socket.gethostname(), 1111))
    marsBaseSocket.listen(2)
    marsSocket, addr = marsBaseSocket.accept()


    #Opening the socket for map operations.
    mapSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mapSocket.connect((socket.gethostname(), 2222))

    while True:
        # This method sends information that will be used for printing the map.
        sendMapCoordinates(rover1, rover2, mapSocket)

        if getMessageViaSocket(11, marsSocket) == "IFAVAILABLE":
            # Prepare the message about the info about rover(s) and send it to the satellite.
            sendRoversInfo(marsBase, rover1, rover2, marsSocket)

            # In this if statement, we need to identify whether a rover is available or not.
            # In order to do that, we look to the first index of info message.
            if determineAvailability():
                # If there is at least one rover available, then get the route info from satellite.
                receiveRoute(marsSocket)

                #If the chosen rover is rover1 then execute this if block.Execute else block otherwise.
                assignRouteToRover(rover1, rover2)
            else:
                # In this else block, we know that satellite wont send any route information because none of
                # them is available. So, we wait for the IFAVAILABLE message again.
                pass
        global messageToSend, route, routeByteLength
        messageToSend = routeByteLength = route = ""

startMarsBaseProcess()

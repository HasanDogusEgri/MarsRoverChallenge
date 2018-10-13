
import socket
import threading
from Satellite import Satellite
import time

receivedMessage = ""


def startSatelliteProcess():
    satelliteProcessThread = threading.Thread(target = SatelliteProcessThread())
    satelliteProcessThread.start()


def sendIfAvailableCommand(socket):
     socket.send("IFAVAILABLE".encode())


def getMessageViaSocket(bufferSize, socket):
    return socket.recv(bufferSize).decode()


def isRoverAvailable():
    if int(receivedMessage[0]) == int(1):
        return True
    else:
        return False


def createAndSendMission(satellite, satelliteSocket):
    mission = satellite.createMission(receivedMessage)
    if len(mission) >= int(10):
        #First message is for sending byte size of buffer.
        #The second message is the mission.
        satelliteSocket.send(str(len(mission)).encode())
        satelliteSocket.send(mission.encode())
    else:
        satelliteSocket.send("0".encode() + str(len(mission)).encode())
        satelliteSocket.send(mission.encode())


def SatelliteProcessThread():

    # Initialization of satellite object.
    satellite = Satellite()

    # Opening the socket for communicating with the base on Mars.
    satelliteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    satelliteSocket.connect((socket.gethostname(), 1111))

    # Opening the socket for map operations.
    mapSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mapSocket.bind((socket.gethostname(), 2222))
    mapSocket.listen(2)
    mapCommunication, addr1 = mapSocket.accept()

    while True:

        global receivedMessage
        receivedMessage = ""
        #This print statement is for refreshing the console.
        print(50 * "\n")

        satellite.printHistory()

        #Send the IFAVAILABLE command to ask whether there exists any available rover.
        sendIfAvailableCommand(satelliteSocket)
        receivedMessage = getMessageViaSocket(5, satelliteSocket)

        if isRoverAvailable():
            #In this case, there is at least a rover available to assign mission.
            createAndSendMission(satellite, satelliteSocket)
        else:
            #In this case, there is no rover that is available at the moment.So we do not assign mission.
            pass

        mapCoordinates = getMessageViaSocket(6,mapCommunication)
        satellite.drawMap(int(mapCoordinates[0]), int(mapCoordinates[1]), int(mapCoordinates[3]), int(mapCoordinates[4]))
        time.sleep(0.5)

startSatelliteProcess()


from SampleFinder import SampleFinder

from Globals import *
class Satellite:

    def __init__(self):
        self.map = [["0"] * PLATEAUXMAX for i in range(PLATEAUYMAX)]
        self.sampleFinder = SampleFinder()
        """
            These additional lines are for creating history of rover-sample and
            showing map.
        """
        self.route1 = self.route2 = ''
        self.sample1X = self.sample1Y = self.sample2X = self.sample2Y = 0
        self.history = [[0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0]]
        self.ct = 0
        self.colorMap = [["0"] * PLATEAUXMAX for i in range(PLATEAUYMAX)]


    def createMission(self, receivedMessage):
        roverX, roverY, face = receivedMessage[1], receivedMessage[2], receivedMessage[3]
        sample = self.sampleFinder.getNextSample()
        route = self.calculateRoute(sample[0], sample[1], roverX, roverY, face)
        """
            These lines except return are for creating map and history.
        """
        #Since we need to save rover-sample tuples, we need to identify
        # which rover is chosen. Then we save the tuple according to chosen rover.
        choice = int(receivedMessage[4])
        if choice == 1:
            self.sample1X, self.sample1Y = sample[0], sample[1]
        else:
            self.sample2X, self.sample2Y = sample[0], sample[1]

        sampleX, sampleY = sample[0], sample[1]
        self.history[self.ct % 5][0] = choice
        self.history[self.ct % 5][1] = sampleX
        self.history[self.ct % 5][2] = sampleY
        self.ct = self.ct + 1

        return route


    def calculateRoute(self,sampleX,sampleY,roverX,roverY,face):
        MOVEMENT=''
        x,y,f=roverX,roverY,face
        x=int(x)
        y=int(y)
        if sampleX!=x:
            if x>sampleX:
                while f!='W':
                    f=DIRECTIONS[DIRECTIONS.index(f)+1]
                    MOVEMENT+='R'
                while x>sampleX:
                    x-=1
                    MOVEMENT+='M'
            else:
                while f!='E':
                    if DIRECTIONS.index(f)>1:
                        f=DIRECTIONS[DIRECTIONS.index(f)-1]
                        MOVEMENT+='L'
                    else:
                        f='E'
                        MOVEMENT+='R'
                while x<sampleX:
                    MOVEMENT+='M'
                    x+=1
        if sampleY!=y:
            if y>sampleY:
                while f!='S':
                    if DIRECTIONS.index(f)<2:
                        f=DIRECTIONS[DIRECTIONS.index(f)+1]
                        MOVEMENT+='R'
                    else:
                        f='S'
                        MOVEMENT+='L'
                while y>sampleY:
                    MOVEMENT+='M'
                    y-=1
            else:
                while f!='N':
                    f=DIRECTIONS[DIRECTIONS.index(f)-1]
                    MOVEMENT+='L'
                while y<sampleY:
                    MOVEMENT+='M'
                    y+=1
        return MOVEMENT


    def createMap(self,x,y,sampleX,sampleY,code):
        y11=y-1
        x11=x
        while x<sampleX:
            self.map[y-1][x]='-'
            self.colorMap[y-1][x]=code
            x=x+1
        while x>sampleX:
            self.map[y-1][x-2]='-'
            self.colorMap[y - 1][x-2] = code
            x=x-1
        while y<sampleY:
            self.map[y][x-1]='|'
            self.colorMap[y][x - 1] = code
            y=y+1
        while y>sampleY:
            self.map[y-2][x-1]='|'
            self.colorMap[y - 2][x - 1] = code
            y=y-1
        if x11>sampleX and y11>sampleY:
            self.map[y11][sampleX-1] = chr(1271)
            self.colorMap[y11][sampleX - 1] = code
        elif x11<sampleX and y11>sampleY:
            self.map[y11][sampleX-1] = chr(741)
            self.colorMap[y11][sampleX - 1] = code
        elif x11>sampleX and y11<sampleY:
            self.map[y11][sampleX-1] = chr(746)
            self.colorMap[y11][sampleX - 1] = code
        elif x11<sampleX and y11<sampleY:
            self.map[y11][sampleX-1] = chr(745)
            self.colorMap[y11][sampleX-1] = code


    def drawMap(self,x1,y1,x2,y2):
        self.map = [[" "] * PLATEAUXMAX for i in range(PLATEAUYMAX)]
        self.colorMap = [["0"] * PLATEAUXMAX for i in range(PLATEAUYMAX)]
        self.createMap(x1, y1, self.sample1X, self.sample1Y, 1)
        self.createMap(x2, y2, self.sample2X, self.sample2Y, 2)
        self.map[y1 - 1][x1 - 1] = 'R'
        self.map[y2 - 1][x2 - 1] = 'T'
        self.map[self.sample1Y - 1][self.sample1X - 1] = 'S'
        self.map[self.sample2Y - 1][self.sample2X - 1] = '$'
        print("-----------------")
        for j in range(PLATEAUYMAX):
            print("|", end = "")
            for i in range(PLATEAUXMAX):
                if self.map[(PLATEAUYMAX - j - 1) % PLATEAUYMAX][i] == "R":
                    prGreen(self.map[(PLATEAUYMAX - j - 1) % PLATEAUYMAX][i])
                elif self.map[(PLATEAUYMAX - j - 1) % PLATEAUYMAX][i] == "T":
                    prPurple(self.map[(PLATEAUYMAX - j - 1) % PLATEAUYMAX][i])
                elif self.map[(PLATEAUYMAX - j - 1) % PLATEAUYMAX][i] == "S":
                    prGreen(self.map[(PLATEAUYMAX - j - 1) % PLATEAUYMAX][i])
                elif self.map[(PLATEAUYMAX - j - 1) % PLATEAUYMAX][i] == "$":
                    prPurple(self.map[(PLATEAUYMAX - j - 1) % PLATEAUYMAX][i])
                elif self.colorMap[(PLATEAUYMAX - j - 1) % PLATEAUYMAX][i] == 1:
                    prGreen(self.map[(PLATEAUYMAX - j - 1) % PLATEAUYMAX][i])
                elif self.colorMap[(PLATEAUYMAX - j - 1) % PLATEAUYMAX][i] == 2:
                    prPurple(self.map[(PLATEAUYMAX - j - 1) % PLATEAUYMAX][i])
                else:
                    prLightGray(" ")
            print("|")
        print("-----------------")


    def printHistory(self):
        for i in range(5):
            print("Rover ID: ", str(self.history[i][0]),
                  "|(X,Y) : (", str(self.history[i][1]), ",", str(self.history[i][2]), ")")

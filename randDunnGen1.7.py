# Random Dungeon Generator 1.7

# Improvements since Random Dungeon Generator 1.0:
    # Added Corridors
    # Updated isIntersecting function which allows for very few intersections
    # Rooms are attempted to be generated multiple times,
    # allowing larger dungeons to be generated.

# Improvements since Random Dungeon Generator 1.1:
    # Added lava pools
    # Added underwater rooms and underlava rooms
        # Underlava rooms are rare!

# Improvements since Random Dungeon Generator 1.2:
    # Improved pool & variants generation

# Improvements since Random Dungeon Generator 1.3:
    # Function that generates a specified number of
    # dungeons and prints out stats about them
        # So far, only does avg num of rooms and
        # average number of doors per room
    # Mode that allows you to watch rooms generate
    # one at a time at intervals of your choice
    # Better room generator: doors, and thus rooms
    # attached to those doors, generate in a random
    # order, so rooms don't just generate in a N, S,
    # E, W fashion

# Improvements since Random Dungeon Generator 1.4:
    # Simple GUI that allows user to repeatedly generate
    # series of dungeons

# Improvements since Random Dungeon Generator 1.5:
    # Made it so that small or thin rooms can't have pools, etc.
    # Added holes (black pools) and pits (black "underwaters")
    # Got rid of the pseudocode
    # Improved the door-shuffling and applied it to start room
    # Improved stats function so that it can tell users the
    # progress it has made in dungeon generation, if wanted

# Improvements since Random Dungeon Generator 1.6:
    # Added square pools, square lava pools, and square holes
        # Only for rectangular rooms, though
    # Improved Statistics function
        # Now Calculates average area per room

# Agenda:
    # Add octagonal rooms
    # Add to GUI so it is more user friendly (Error Catching)
    # Add different types of specs (traps, chests, etc.)
    # Add to function that analyzes a bunch of dungeons for stats
    # so that proabilities of certain room types, such as corridors,
    # pool rooms etc. can be determined
    # Far future:
        # Add different levels to each dungeon
        # Create 'customized' dungeon type like buffet world
        # type in Minecraft (preferrable through GUI)
        # Add sprites, like monsters, that move around in their rooms
        

from graphics import *
from random import *
from time import *
from math import pi

# Note to self: random() returns a random no. in the interval [0,1)

class MyError(Exception):
    pass

class RoomError(MyError):

    def __init__(self,message):
        self.message = message


class Danger(MyError):
    def __init__(self,message):
        self.message = message

def duplicates(element,aList): # returns True if duplicates of element in aList
    numElement = 0 
    for i in aList:
        if i == element:
            numElement += 1
    if numElement >= 2:
        return True
    else:
        return False

def anyDup(aList): #returns True if any duplicates in aList
    for element in aList:
        if duplicates(element,aList):
            return True
    return False

def avgTwo(num1,num2): #returns average of two nums
    return (num1+num2)/2

def inBetween(aValue,aList): 
    # checks to see if aValue is between the first two value in aList
    if aList[0] < aValue < aList[1]:
        return True
    else:
        return False

def tenRange(minValue,maxValue):
    """Returns list of 11 values from minValue to maxValue
with equal spacing"""
    incriment = (maxValue-minValue)/10
    resultList = []
    for var in range(11):
        resultList.append(minValue+var*incriment)
    return resultList

def shuffle(aList):
    # Used to randomize door lists
    newList = [""]*len(aList)
    for element in aList:
        pos = randrange(len(aList))
        while newList[pos] != "":
            pos = randrange(len(aList))
        newList[pos] = element
    return newList

class Room:

    """xMin, yMin, etc. refer to the bounding points of the room
which no other room can enter. shape is a string, either 'rectangle'
or 'oval'. doorDirections should be a list of the characters 'N', 'E',
'S' and 'W' which describe which walls of the room have doors
no duplicates). window should be a GraphWin. spec refers to anything
special about the room."""

    #Note to self: No more separate corridor type. Instead, they are
    #rectangles with a self.xLen or self.yLen of 20 (for 10 ft wide corridor)

    def __init__(self,xMin,yMin,xMax,yMax,shape,doorDirections,window,spec=""):
        if xMin > xMax or yMin > yMax:
            raise RoomError("Minimums cannot be larger than Maximums!")
        if shape not in ["rectangle","oval"]:
            raise RoomError("Shape not valid.")
        for char in doorDirections:
            if char not in ['W','N','E','S']:
                raise RoomError("Door Directions must be 'N','E','W',or'S'.")
        if anyDup(doorDirections):
            raise RoomError("Only one door per wall is possible.")
        if spec not in ["","pool","lava pool","underwater","underlava",
                        "hole","pit","square pool","square lava pool",
                        "square hole"]:
            raise RoomError("Invalid value for 'spec'.")
        self.xRange = [xMin,xMax]
        self.yRange = [yMin,yMax]
        self.shape = shape
        self.doors = doorDirections
        self.xLen = self.xRange[1]-self.xRange[0]
        self.yLen = self.yRange[1]-self.yRange[0]
        self.xMidPt = (self.xRange[0]+self.xRange[1])/2
        self.yMidPt = (self.yRange[0]+self.yRange[1])/2
        self.xBigRange = tenRange(xMin,xMax) #[xMin,self.xMidPt,xMax]
        self.yBigRange = tenRange(yMin,yMax) #[yMin,self.yMidPt,yMax]
        self.win = window
        self.spec = spec

    def drawDoors(self): #Helper function
        for door in self.doors:
            if door == 'N':
                rect = Rectangle(Point(self.xMidPt-5,self.yRange[0]-5),
                                 Point(self.xMidPt+5,self.yRange[0]+5))
                rect.draw(self.win)
            elif door == 'S':
                rect = Rectangle(Point(self.xMidPt-5,self.yRange[1]-5),
                                 Point(self.xMidPt+5,self.yRange[1]+5))
                rect.draw(self.win)
            elif door == 'W':
                rect = Rectangle(Point(self.xRange[0]-5,self.yMidPt-5),
                                 Point(self.xRange[0]+5,self.yMidPt+5))
                rect.draw(self.win)
            elif door == 'E':
                rect = Rectangle(Point(self.xRange[1]-5,self.yMidPt-5),
                                 Point(self.xRange[1]+5,self.yMidPt+5))
                rect.draw(self.win)
                
    def draw(self):
        
        if self.shape == "rectangle":
            xMin = self.xRange[0]+5
            xMax = self.xRange[1]-5
            yMin = self.yRange[0]+5
            yMax = self.yRange[1]-5
            rect = Rectangle(Point(xMin,yMin),Point(xMax,yMax))
            if self.spec == "underwater":
                rect.setFill("blue")
            if self.spec == "underlava":
                rect.setFill("red")
            if self.spec == "pit":
                rect.setFill("black")
            rect.draw(self.win)
        elif self.shape == "oval":
            xMin = self.xRange[0]+5
            xMax = self.xRange[1]-5
            yMin = self.yRange[0]+5
            yMax = self.yRange[1]-5
            oval = Oval(Point(xMin,yMin),Point(xMax,yMax))
            if self.spec == "underwater":
                oval.setFill("blue")
            if self.spec == "underlava":
                oval.setFill("red")
            if self.spec == "pit":
                oval.setFill("black")
            oval.draw(self.win)
        else:
            raise RoomError("Shape not valid.")
        
        self.drawDoors()

        if self.spec == "pool":
            center = Point(avgTwo(self.xRange[0],self.xRange[1]),
                           avgTwo(self.yRange[0],self.yRange[1]))
            rad = min(self.xLen,self.yLen)/2 - 15
            circ = Circle(center,rad)
            circ.setFill("blue")
            circ.draw(self.win)
        elif self.spec == "square pool":
            c = Point(avgTwo(self.xRange[0],self.xRange[1]),
                           avgTwo(self.yRange[0],self.yRange[1]))
            r = min(self.xLen,self.yLen)/2 - 15
            lr = Point(c.getX()+r,c.getY()+r)
            ul = Point(c.getX()-r,c.getY()-r)
            sqr = Rectangle(ul,lr)
            sqr.setFill("blue")
            sqr.draw(self.win)
        elif self.spec == "lava pool":
            center = Point(avgTwo(self.xRange[0],self.xRange[1]),
                           avgTwo(self.yRange[0],self.yRange[1]))
            rad = min(self.xLen,self.yLen)/2 - 15
            circ = Circle(center,rad)
            circ.setFill("red")
            circ.draw(self.win)
        elif self.spec == "square lava pool":
            c = Point(avgTwo(self.xRange[0],self.xRange[1]),
                           avgTwo(self.yRange[0],self.yRange[1]))
            r = min(self.xLen,self.yLen)/2 - 15
            lr = Point(c.getX()+r,c.getY()+r)
            ul = Point(c.getX()-r,c.getY()-r)
            sqr = Rectangle(ul,lr)
            sqr.setFill("red")
            sqr.draw(self.win)
        elif self.spec == "hole":
            center = Point(avgTwo(self.xRange[0],self.xRange[1]),
                           avgTwo(self.yRange[0],self.yRange[1]))
            rad = min(self.xLen,self.yLen)/2 - 15
            circ = Circle(center,rad)
            circ.setFill("black")
            circ.draw(self.win)
        elif self.spec == "square hole":
            c = Point(avgTwo(self.xRange[0],self.xRange[1]),
                           avgTwo(self.yRange[0],self.yRange[1]))
            r = min(self.xLen,self.yLen)/2 - 15
            lr = Point(c.getX()+r,c.getY()+r)
            ul = Point(c.getX()-r,c.getY()-r)
            sqr = Rectangle(ul,lr)
            sqr.setFill("black")
            sqr.draw(self.win)
        elif (self.spec == "" or self.spec == "underwater" or
              self.spec == "underlava" or self.spec == "pit"):
            pass
        else:
            raise RoomError("Invalid spec")


    def inBoundaries(self,x,y):
        if inBetween(x,self.xRange) and inBetween(y,self.yRange):
            return True
        else:
            return False

    def getArea(self):
        if self.shape == "rectangle":
            return self.xLen * self.yLen
        elif self.shape == "oval":
            return 0.25 * pi * self.xLen * self.yLen
        else:
           raise RoomError("Shape not valid.") 





def randBool(weight = 0.5):
    x = random()
    if x < weight:
        return 0
    else:
        return 1

def randPool():
    # Returns whether room has pool and features
    if randBool(0.2):
        return ""
    else:
        if randBool(0.2):
            if randBool(0.2):
                if randBool(1/3):
                    if randBool(1/3):
                        return "pool"
                    else:
                        return "square pool"
                else:
                    if randBool(1/3):
                        return "hole"
                    else:
                        return "square hole"
            else:
                if randBool():
                    return "underwater"
                else:
                    return "pit"
        else:
            if randBool(0.2):
                if randBool(1/3):
                    return "lava pool"
                else:
                    return "square lava pool"
            else:
                return "underlava"

def randSpecs(startDoor=""):
    
    """startDoor is usally 'N','S','E',or 'W'
but can be '' if it is the starting room"""
    isNotCorridor = randBool() 
    if isNotCorridor:
        length = 30 + 120*random()
        width = 30 + 120*random()
        shapeList = ["rectangle","oval"]
        shape = shapeList[randBool()]
        if length > 40 and width > 40:
            spec = randPool()
            # So square pools and variants aren't supported by oval rooms:
            if shape == "oval":
                if spec == "square pool":
                    spec = "pool"
                if spec == "square hole":
                    spec = "hole"
                if spec == "square lava pool":
                    spec = "lava pool"
        else:
            spec = ""
    else:
        if randBool(): # E/W or N/S
            length = 30
            width = 150+100*random()
        else:
            length = 150+100*random()
            width = 30
        shape = "rectangle"
        spec = ""
    doorList = [startDoor]
    if startDoor == "":
        doorList = []
    for door in ["N","S","E","W"]:
        if (door != startDoor) and (randBool(0.25)):
            doorList = doorList + [door]
    doorList = shuffle(doorList)
    return [length,width,shape,doorList,spec]
    
def createRandRoom(otherRoom,otherDoor):
    oldSpecs = randSpecs(otherDoor)
    if otherDoor == "N":
        myDoor = "S"
        yMax = otherRoom.yRange[0]
        yMin = yMax - oldSpecs[1]
        xMid = otherRoom.xMidPt
        xMin = xMid - oldSpecs[0]/2
        xMax = xMid + oldSpecs[0]/2
        window = otherRoom.win
        return Room(xMin,yMin,xMax,yMax,oldSpecs[2],oldSpecs[3],window,oldSpecs[4])
    elif otherDoor == "S":
        myDoor = "N"
        yMin = otherRoom.yRange[1]
        yMax = yMin + oldSpecs[1]
        xMid = otherRoom.xMidPt
        xMin = xMid - oldSpecs[0]/2
        xMax = xMid + oldSpecs[0]/2
        window = otherRoom.win
        return Room(xMin,yMin,xMax,yMax,oldSpecs[2],oldSpecs[3],window,oldSpecs[4])
    elif otherDoor == "W":
        myDoor = "E"
        xMax = otherRoom.xRange[0]
        xMin = xMax - oldSpecs[0]
        yMid = otherRoom.yMidPt
        yMin = yMid - oldSpecs[1]/2
        yMax = yMid + oldSpecs[1]/2
        window = otherRoom.win
        return Room(xMin,yMin,xMax,yMax,oldSpecs[2],oldSpecs[3],window,oldSpecs[4])
    elif otherDoor == "E":
        myDoor = "W"
        xMin = otherRoom.xRange[1]
        xMax = xMin + oldSpecs[0]
        yMid = otherRoom.yMidPt
        yMin = yMid - oldSpecs[1]/2
        yMax = yMid + oldSpecs[1]/2
        window = otherRoom.win
        return Room(xMin,yMin,xMax,yMax,oldSpecs[2],oldSpecs[3],window,oldSpecs[4])
    elif otherDoor == "" and otherRoom == "N/A":
        # This is in case of starting room; come back later if necessary
        pass
    else:
        raise RoomError("Invalid Room.")


def isIntersecting(room1,room2):
    for xCoord in room2.xBigRange:
        for yCoord in room2.yBigRange:
            if room1.inBoundaries(xCoord,yCoord):
                return True
    for xCoord in room1.xBigRange:
        for yCoord in room1.yBigRange:
            if room2.inBoundaries(xCoord,yCoord):
                return True
    return False

class Dungeon:

    """A way to store rooms in a list, which can be modified
by an external function."""

    def __init__(self,roomList,window):
        self.roomList = roomList
        self.win = window

    def getRooms(self):
        return self.roomList

    def getWin(self):
        return self.win

    def close(self):
        self.win.close()

    def numRooms(self):
        return len(self.roomList)

    # These next methods for Dungeon class are not implimented yet

    def shapeList(self):
        """Returns list of shapes of the rooms"""
        shapes = []
        for room in self.roomList:
            shapes.append(room.shape)
        return shapes

    def numOfDoorsList(self):
        """Returns list of number of doors for each room"""
        numDoors = []
        for room in self.roomList:
            numDoors.append(len(room.doors))
        return numDoors

    def numDoors(self):
        numDoors = []
        for room in self.roomList:
            numDoors.append(len(room.doors))
        total = 0
        for room in numDoors:
            total += room
        return total

    def getTotArea(self):
        total = 0
        for room in self.roomList:
            total += room.getArea()
        return total

def isOutOfDunBounds(room,dungeon):
    for xCoord in room.xRange:
        if not inBetween(xCoord,[0,dungeon.win.width]):
            return True
    for yCoord in room.yRange:
        if not inBetween(yCoord,[0,dungeon.win.height]):
            return True
    return False

def canMakeRoom(room,dungeon):
    for aRoom in dungeon.roomList:
        if isIntersecting(aRoom,room):
            return False
    if isOutOfDunBounds(room,dungeon):
        return False
    return True

def dunCheck(dungeon):
    for room in dungeon.roomList:
        roomList = dungeon.roomList[:]
        roomList.remove(room)
        for otherRoom in roomList:
            if isIntersecting(room,otherRoom):
                return "Error"

def makeRandDun(dungeon,startRoom,doorFrom="",attempts=3,pause=False): 
    doorList = startRoom.doors
    if doorFrom in doorList:
        doorList.remove(doorFrom)
    for door in doorList:
        counter = 0
        roomNotMade = True
        while counter < attempts and roomNotMade:
            newRoom = createRandRoom(startRoom,door)
            if canMakeRoom(newRoom,dungeon):
                sleep(pause)
                newRoom.draw()
                dungeon.roomList.append(newRoom)
                makeRandDun(dungeon,newRoom,door,attempts,pause)
                roomNotMade = False
            counter = counter + 1

def main(num=1,att=3,pause=0):
    if num > 100:
        raise Danger("You could have crashed your computer")
    for i in range(num):
        myWin = GraphWin("My Dungeon",1500,750)
        startDoors = shuffle(["N","S","E","W"])
        startRoom = Room(700,325,800,425,"rectangle",startDoors,myWin)
        startRoom.draw()
        myDun = Dungeon([startRoom],myWin)
        makeRandDun(myDun,startRoom,"",att,pause)
        dunCheck(myDun)

def collectStats(num=100,att=3,showProgress=False): # Work in progress
    totRooms = 0
    totDoors = 0
    totArea = 0
    for i in range(num):
        myWin = GraphWin("My Dungeon",1500,750)
        startDoors = shuffle(["N","S","E","W"])
        startRoom = Room(700,325,800,425,"rectangle",startDoors,myWin)
        startRoom.draw()
        myDun = Dungeon([startRoom],myWin)
        makeRandDun(myDun,startRoom,"",att)
        dunCheck(myDun)
        totRooms += myDun.numRooms()
        totDoors += myDun.numDoors()
        totArea += myDun.getTotArea()
        myDun.close()
        if showProgress:
            print("Dungeons Completed: ",i+1," out of ",num)
    print("\nThe avg num of rooms per dungeon is:",totRooms/num)
    print("The avg num of doors per room is:",totDoors/totRooms)
    print("The avg amount of area per room is:",totArea/totRooms,"\n")
    

def myTest(door):
	myWin = GraphWin("Test",500,500)
	start = Room(200,200,300,300,"rectangle",["N","S","E","W"],myWin)
	start.draw()
	newRoom = createRandRoom(start,door)
	newRoom.draw()
	return [myWin,start,newRoom] 

def guiMain(): # WIP
    gui = GraphWin("Dungeon Generator 1.5",500,500)
    text1 = Text(Point(250,100),"How many dungeons?")
    text1.draw(gui)
    entry1 = Entry(Point(250,125),3)
    entry1.draw(gui)
    text2 = Text(Point(250,150),"How many attempts per room?")
    text2.draw(gui)
    entry2 = Entry(Point(250,175),1)
    entry2.draw(gui)
    text3 = Text(Point(250,200),"How many seconds to pause between rooms?")
    text3.draw(gui)
    entry3 = Entry(Point(250,225),5)
    entry3.draw(gui)
    text4 = Text(Point(250,250),"Click the screen when you are done.")
    text4.draw(gui)
    gui.getMouse()
    dun = eval(entry1.getText())
    att = eval(entry2.getText())
    pause = eval(entry3.getText())
    gui.close()
    main(dun,att,pause)
    # Ask again here
    gui = GraphWin("Dungeon Generator 1.5",500,500)
    text1 = Text(Point(250,100),"Do you want to generate more dungeons?")
    text1.draw(gui)
    entry1 = Entry(Point(250,125),3)
    entry1.draw(gui)
    text4 = Text(Point(250,250),"Click the screen when you are done.")
    text4.draw(gui)
    gui.getMouse()
    theInput = entry1.getText()
    if theInput[0] == "y":
        gui.close()
        guiMain()
    gui.close()
    # Next thing to do: make more user friendly by catching errors
    # (Such as when user clicks screen before they enter all their info)

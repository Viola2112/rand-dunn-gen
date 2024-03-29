# Random Dungeon Generator 1.3

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

# Agenda: add octagonal rooms, and mode in which you can see rooms
# appearing one at a time in 1-sec intervals
# Make a function that analyzes a bunch of dungeons for stats
# Far future: add different levels to each dungeon

from graphics import *
from random import *

# Note to self: random() returns a random no. in the interval [0,1)

class MyError(Exception):
    pass

class RoomError(MyError):

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
        if shape not in ["rectangle","oval",]:
            raise RoomError("Shape not valid.")
        for char in doorDirections:
            if char not in ['W','N','E','S']:
                raise RoomError("Door Directions must be 'N','E','W',or'S'.")
        if anyDup(doorDirections):
            raise RoomError("Only one door per wall is possible.")
        if spec not in ["","pool","lava pool","underwater","underlava"]:
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
        
        #if self.shape == "circle":
            #center = Point(avgTwo(self.xRange[0],self.xRange[1]),
                           #avgTwo(self.yRange[0],self.yRange[1]))
            #rad = min(self.xLen,self.yLen)/2 - 5
            #circ = Circle(center,rad)
            #circ.draw(self.win)
        #elif self.shape == "square":
            #pass
        
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
            oval.draw(self.win)
        #elif self.shape == "corridor":
            #pass
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
        elif self.spec == "lava pool":
            center = Point(avgTwo(self.xRange[0],self.xRange[1]),
                           avgTwo(self.yRange[0],self.yRange[1]))
            rad = min(self.xLen,self.yLen)/2 - 15
            circ = Circle(center,rad)
            circ.setFill("red")
            circ.draw(self.win)
        elif (self.spec == "" or self.spec == "underwater" or
              self.spec == "underlava"):
            pass
        else:
            raise RoomError("Invalid spec")


    def inBoundaries(self,x,y):
        if inBetween(x,self.xRange) and inBetween(y,self.yRange):
            return True
        else:
            return False



###############################################
        # This section of the program wil be set aside
        # as space to figure out an alogrithm to create
        # a random room.

        #Pseudocode:

        # Create a function with the following arguments:
            # List of the rooms in the dungeon
            # The current room
            # The GraphWin in which the dungeon is contained
            # Any doors from which the room was generated
        # The function will do the following:
            # For each of the doors the room has NOT been created from:
                # Generate a set of random specs for a new room (or corridor)
                    # These include shape, len, width, center, doors, 
                    # and whether the room has a pool or not.
                # Check to see if the room can be generated
                    # The room must be inside the graphwin and not
                    # enter the spaces of any other rooms.
                # If the room can be generated:                
                    # Create an object for the room
                    # Add the room to the room list
                        # Problem: can't change argument in Python! Carp
                        # Possible solution: use a class instead of
                        # a method to store info about dungeon. Note that
                        # the created function cannot be one of the class's
                        # methods, but an exterior method, as a class can't
                        # have a recursive fn inside of it. Also, the
                        # "room list" argument of the fn will be the class,
                        # not an actual list.
                    # Draw the room
                    # Carry out the function again for this door
                        # Recursive Function!
                # If the toom cannot be generated:
                    # Do nothing
        # Eventually, the program should stop, as it cannot create
        # a room if there is not enough space.

        # Optional afterwards:
            # Allow user to input a "seed" value or
            # specify how common certain types of rooms are
            # like "Customized" world type in Minecraft.
            
###############################################

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
                return "pool"
            else:
                return "underwater"
        else:
            if randBool(0.2):
                return "lava pool"
            else:
                return "underlava"

def randSpecs(startDoor=""):
    # Some overlap issues for corridors;
    # May need to change intersection fn
    # To check more points
    
    """startDoor is usally 'N','S','E',or 'W'
but can be '' if it is the starting room"""
    isNotCorridor = randBool() #May need to change
    if isNotCorridor:
        length = 30 + 120*random()
        width = 30 + 120*random()
        shapeList = ["rectangle","oval"]
        shape = shapeList[randBool()]
        spec = randPool()
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

def makeRandDun(dungeon,startRoom,doorFrom="",attempts=3): 
    doorList = startRoom.doors
    if doorFrom in doorList:
        doorList.remove(doorFrom)
    for door in doorList:
        counter = 0
        roomNotMade = True
        while counter < attempts and roomNotMade:
            newRoom = createRandRoom(startRoom,door)
            if canMakeRoom(newRoom,dungeon):
                newRoom.draw()
                dungeon.roomList.append(newRoom)
                makeRandDun(dungeon,newRoom,door)
                roomNotMade = False
            counter = counter + 1

def main(num=1,att=3):
    for i in range(num):
        myWin = GraphWin("My Dungeon",1500,750)
        startRoom = Room(700,325,800,425,"rectangle",["N","S","E","W"],myWin)
        startRoom.draw()
        myDun = Dungeon([startRoom],myWin)
        makeRandDun(myDun,startRoom,"",att)
        dunCheck(myDun)
    

def myTest(door):
	myWin = GraphWin("Test",500,500)
	start = Room(200,200,300,300,"rectangle",["N","S","E","W"],myWin)
	start.draw()
	newRoom = createRandRoom(start,door)
	newRoom.draw()
	return [myWin,start,newRoom]



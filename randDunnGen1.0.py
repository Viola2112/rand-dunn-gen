# Random Dungeon Generator

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

def inBetween(aValue,aList): #Note to self: change back to < < if <= <= doesn't work
    # checks to see if aValue is between the first two value in aList
    if aList[0] < aValue < aList[1]:
        return True
    else:
        return False

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
        if spec not in ["","pool"]:
            raise RoomError("Invalid value for 'spec'.")
        self.xRange = [xMin,xMax]
        self.yRange = [yMin,yMax]
        self.shape = shape
        self.doors = doorDirections
        self.xLen = self.xRange[1]-self.xRange[0]
        self.yLen = self.yRange[1]-self.yRange[0]
        self.xMidPt = (self.xRange[0]+self.xRange[1])/2
        self.yMidPt = (self.yRange[0]+self.yRange[1])/2
        self.xBigRange = [xMin,self.xMidPt,xMax]
        self.yBigRange = [yMin,self.yMidPt,yMax]
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
            rect.draw(self.win)
        elif self.shape == "oval":
            xMin = self.xRange[0]+5
            xMax = self.xRange[1]-5
            yMin = self.yRange[0]+5
            yMax = self.yRange[1]-5
            oval = Oval(Point(xMin,yMin),Point(xMax,yMax))
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
        elif self.spec == "":
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

def randSpecs(startDoor=""): #Might want to add corridors
    
    """startDoor is usally 'N','S','E',or 'W'
but can be '' if it is the starting room"""
    
    length = 25 + 125*random()
    width = 25 + 125*random()
    shapeList = ["rectangle","oval"]
    shape = shapeList[randBool()]
    doorList = [startDoor]
    if startDoor == "":
        doorList = []
    for door in ["N","S","E","W"]:
        if (door != startDoor) and (randBool(0.25)):
            doorList = doorList + [door]
    specList = ["","pool"]
    spec = specList[randBool(0.8)]
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

def makeRandDun(dungeon,startRoom,doorFrom=""): #Almost works, but some rooms intersect
    # I think I need to make it so a room can't generate a room
    # in the direction from which it came, and then it will work
    #ughhhhhhhhhhhhh still doesn't work-may need to change intersecion fn
    #might have to do with doorFrom too
    doorList = startRoom.doors
    if doorFrom in doorList:
        doorList.remove(doorFrom)
    for door in doorList:
        newRoom = createRandRoom(startRoom,door)
        if canMakeRoom(newRoom,dungeon):
            newRoom.draw()
            dungeon.roomList.append(newRoom)
            makeRandDun(dungeon,newRoom,door)

def main(num=1):
    for i in range(num):
        myWin = GraphWin("My Dungeon",1500,750)
        startRoom = Room(700,325,800,425,"rectangle",["N","S","E","W"],myWin)
        startRoom.draw()
        myDun = Dungeon([startRoom],myWin)
        makeRandDun(myDun,startRoom)
        dunCheck(myDun)
    

def myTest(door):
	myWin = GraphWin("Test",500,500)
	start = Room(200,200,300,300,"rectangle",["N","S","E","W"],myWin)
	start.draw()
	newRoom = createRandRoom(start,door)
	newRoom.draw()
	return [myWin,start,newRoom]

# Next thing to do: make a fn which tells if two rooms intersect
# This function has been created; two adjacent rooms generated by room
# generator are not intersecting, but the fn needs to be tested more
# 1-27-19: It works!!!! I have also made a function which tests whether
# a given room in a dungeon can be created.
# Next thing to do: make "mother" function to generate the whole dungeon!

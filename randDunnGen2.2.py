# Random Dungeon Generator 2.2

# Last updated: 9/12/2019

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

# Improvements since Random Dungeon Generator 1.7:
    # Added octagon rooms
        # Always have same xLen and yLen
    # Put more limitations on num and att for main function
        # To prevent from accidentally crashing computer
    # Made pits more rare and underwater rooms more common

# Improvements since Random Dungeon Generator 1.8:
    # Customized now functional, with a few presets!
        # Size and direction of corridors will not be changed -- yet

# Improvements since Random Dungeon Generator 2.0:
    # Size of corridors now customizable
        # Only 1 preset for it so far though
    # Simple Text-Based Interface
        # Does not cover all features of main() though

# Improvements since Random Dungeon Generator 2.1:
    # Small fixes to GUI to display version correctly
    # Updated Text-Based Interface
        # Now includes presets and customization
        # Not generalized to GUI yet
        # Doesn't allow saving of dungeons yet

# Agenda:
    # Add to GUI so it is more user friendly (Error Catching)
    # Include presets in GUI
    # Add different types of specs (traps, chests, etc.)
    # Add to function that analyzes a bunch of dungeons for stats
    # so that proabilities of certain room types, such as corridors,
    # pool rooms etc. can be determined and add standard deviation
    # Far future:
        # Add different levels to each dungeon
        # Add sprites, like monsters, that move around in their rooms
        # Instead of using python's ramdom function, make a seperate
        # chaos function which grows from a certain seed, and use this
        # to generate whole dungeon from one number, like in Minecraft
            # For this, I could delete the "from random import *" statement
            # and make custom random() and randrange methods.
        # Be able to save/delete dungeons.
        

from graphics import *
from random import *
from time import *
from math import pi

VERSION = "2.2"

######################################################################
# Global Variables for "Seeds"

POOL_SEED = [0.2,0.2,0.2,1/3,1/3]
    # POOL_SEED[0] affects chance of feature at all
    # POOL_SEED[1] affects chance of lava
    # POOL_SEED[2] affects chance of under___
    # POOL_SEED[3] affects chance of water vs. pit
    # POOL_SEED[4] affects chance of square

SHAPE_SEED = [0.5,2,2,1]
    # SHAPE_SEED[0] affects chance of corridor
    # SHAPE_SEED[1] is relative frequency of rectangles
    # SHAPE_SEED[2] is relative frequency of ovals
    # SHAPE_SEED[3] is relative frequency of octagons

SIZE_SEED = [30,120,30,120,30,150,100]
    # SIZE_SEED[0] is length minimum
    # SIZE_SEED[1] is length range
    # SIZE_SEED[2] is width minimum
    # SIZE_SEED[3] is width range
    # Next elements are for corridors:
    # SIZE_SEED[4] is short side length
    # SIZE_SEED[5] is long side minimum
    # SIZE_SEED[6] iS long side range

SEED_LIST = [POOL_SEED,SHAPE_SEED,SIZE_SEED]

# Some Presets:

LAVA_LAND = [[0.2,1,0.2,1/3,1/3],SHAPE_SEED,SIZE_SEED]
LAVA_MANIA = [[1,1,0.2,1/3,1/3],SHAPE_SEED,SIZE_SEED]
NO_CORRIDORS = [POOL_SEED,[0,2,2,1],SIZE_SEED]
ONLY_CORRIDORS = [POOL_SEED,[1,2,2,1],SIZE_SEED]
LOTS_O_OCTO = [POOL_SEED,[0.5,1,1,2],SIZE_SEED]
ALWAYS_FEATURES = [[1,0.2,0.2,1/3,1/3],SHAPE_SEED,SIZE_SEED]
OCEAN = [[1,0,1,0,0],SHAPE_SEED,SIZE_SEED]
LAVA_OCEAN = [[1,1,1,0,0],SHAPE_SEED,SIZE_SEED]
MEGA_ROOMS = [POOL_SEED,SHAPE_SEED,[45,180,45,180,30,150,100]]
MINI_ROOMS = [POOL_SEED,SHAPE_SEED,[20,80,20,80,30,150,100]]
LONG_CORRIDORS = [POOL_SEED,SHAPE_SEED,[30,120,30,120,30,225,150]]
SHORT_CORRIDORS = [POOL_SEED,SHAPE_SEED,[30,120,30,120,30,100,200/3]]

PRESET_NAMES = ["LAVA_LAND","LAVA_MANIA","NO_CORRIDORS",
                "ONLY_CORRIDORS","LOTS_O_OCTO","ALWAYS_FEATRUES",
                "OCEAN","LAVA_OCEAN","MEGA_ROOMS","MINI_ROOMS",
                "LONG_CORRIDORS","SHORT_CORRIDORS"]
    
######################################################################
# Rest of program starts here

# Note to self: random() returns a random no. in the interval [0,1)

class MyError(Exception):
    pass

class RoomError(MyError):

    def __init__(self,message):
        self.message = message

class AlexError(MyError): # Put in here as joke

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
        if shape not in ["rectangle","oval","octagon"]:
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
        elif self.shape == "octagon": 
            xMin = self.xRange[0]+5
            xMax = self.xRange[1]-5
            yMin = self.yRange[0]+5
            yMax = self.yRange[1]-5
            xMid1 = 2*xMin/3 + xMax/3
            xMid2 = 2*xMax/3 + xMin/3
            yMid1 = 2*yMin/3 + yMax/3
            yMid2 = 2*yMax/3 + yMin/3
            octagon = Polygon(Point(xMid1,yMin),Point(xMid2,yMin),
                              Point(xMax,yMid1),Point(xMax,yMid2),
                              Point(xMid2,yMax),Point(xMid1,yMax),
                              Point(xMin,yMid2),Point(xMin,yMid1))
            if self.spec == "underwater":
                octagon.setFill("blue")
            if self.spec == "underlava":
                octagon.setFill("red")
            if self.spec == "pit":
                octagon.setFill("black")
            octagon.draw(self.win)
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
        elif self.shape == "octagon":
            return self.xLen * self.yLen * (7/9)
        else:
           raise RoomError("Shape not valid.") 





def randBool(weight = 0.5):
    x = random()
    if x < weight:
        return 0
    else:
        return 1

def randPool(seed=POOL_SEED):
    # Returns whether room has pool and features
    if randBool(seed[0]):
        # No pool
        return ""
    else:
        if randBool(seed[1]):
            # Water or hole/pit
            if randBool(seed[2]):
                # Circular or square pool/hole
                if randBool(seed[3]):
                    # Pool
                    if randBool(seed[4]):
                        return "pool"
                    else:
                        return "square pool"
                else:
                    # Hole
                    if randBool(seed[4]):
                        return "hole"
                    else:
                        return "square hole"
            else:
                # Underwater/pit
                if randBool(seed[3]):
                    return "underwater"
                else:
                    return "pit"
        else:
            # Has Lava
            if randBool(seed[2]):
                # Circular/Square lava pool
                if randBool(seed[4]):
                    return "lava pool"
                else:
                    return "square lava pool"
            else:
                return "underlava"

def randSpecs(startDoor="",seedList=SEED_LIST):
    
    """startDoor is usally 'N','S','E',or 'W'
but can be '' if it is the starting room"""

    poolSeed = seedList[0]
    shapeSeed = seedList[1]
    sizeSeed = seedList[2]
    
    isNotCorridor = randBool(shapeSeed[0]) 
    if isNotCorridor:
        length = sizeSeed[0] + sizeSeed[1]*random()
        width = sizeSeed[2] + sizeSeed[3]*random()
        shapeList = (["rectangle"]*shapeSeed[1] + ["oval"]*shapeSeed[2] +
                     ["octagon"]*shapeSeed[3])
        shape = shapeList[randrange(len(shapeList))]
        if shape == "octagon":
            length = width # To make octagonal rooms symmetrical
        if length > 40 and width > 40:
            spec = randPool(poolSeed)
            if shape == "oval" or shape == "octagon":
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
            length = sizeSeed[4]
            width = sizeSeed[5]+sizeSeed[6]*random()
        else:
            length = sizeSeed[5]+sizeSeed[6]*random()
            width = sizeSeed[4]
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
    
def createRandRoom(otherRoom,otherDoor,seedList=SEED_LIST):
    oldSpecs = randSpecs(otherDoor,seedList)
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

def makeRandDun(dungeon,startRoom,doorFrom="",attempts=3,pause=False,seedList=SEED_LIST): 
    doorList = startRoom.doors
    if doorFrom in doorList:
        doorList.remove(doorFrom)
    for door in doorList:
        counter = 0
        roomNotMade = True
        while counter < attempts and roomNotMade:
            newRoom = createRandRoom(startRoom,door,seedList)
            if canMakeRoom(newRoom,dungeon):
                sleep(pause)
                newRoom.draw()
                dungeon.roomList.append(newRoom)
                makeRandDun(dungeon,newRoom,door,attempts,pause,seedList)
                roomNotMade = False
            counter = counter + 1

def main(num=1,att=3,pause=0,seedList=SEED_LIST):
    if num > 100 or att > 100 or (num*att)>1000:
        raise Danger("You could have crashed your computer")
    for i in range(num):
        myWin = GraphWin("My Dungeon",1500,750)
        startDoors = shuffle(["N","S","E","W"])
        startRoom = Room(700,325,800,425,"rectangle",startDoors,myWin)
        startRoom.draw()
        myDun = Dungeon([startRoom],myWin)
        makeRandDun(myDun,startRoom,"",att,pause,seedList)
        dunCheck(myDun)

def collectStats(num=100,att=3,showProgress=False,seedList=SEED_LIST): # WIP
    totRooms = 0
    totDoors = 0
    totArea = 0
    for i in range(num):
        myWin = GraphWin("My Dungeon",1500,750)
        startDoors = shuffle(["N","S","E","W"])
        startRoom = Room(700,325,800,425,"rectangle",startDoors,myWin)
        startRoom.draw()
        myDun = Dungeon([startRoom],myWin)
        makeRandDun(myDun,startRoom,"",att,0,seedList)
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

def printIntro():
    print("Welcome to Dungeon Generator",VERSION,"!")
    print("This program generates random dungeons for")
    print("your pleasure based on your inputs such as")
    print("how many dungeons you want, how many times")
    print("the program should attempt to make the room,")
    print("and so on.")

def getCustomSeed():
    """Get completely customized seed from user"""
    poolSeed = []
    shapeSeed = []
    sizeSeed = []
    theIn = input("Would you like to use the standard pool preset? ")
    if theIn[0] == "y" or theIn[0] == "Y":
        poolSeed = POOL_SEED
    else:
        temp = eval(input("Chance of feature/room: (Default 0.2) "))
        poolSeed.append(temp)
        temp = eval(input("Chance of lava/pool: (Default 0.2) "))
        poolSeed.append(temp)
        temp = eval(input("Chance of under___/pool: (Default 0.2) "))
        poolSeed.append(temp)
        temp = eval(input("Chance of pit/pool: (Default 1/3) "))
        poolSeed.append(temp)
        temp = eval(input("Chance of square/pool: (Default 1/3) "))
        poolSeed.append(temp)
    theIn = input("Would you like to use the standard shape preset? ")
    if theIn[0] == "y" or theIn[0] == "Y":
        shapeSeed = SHAPE_SEED
    else:
        temp = eval(input("Chance of corridor: (Default 0.5) "))
        shapeSeed.append(temp)
        temp = eval(input("Relative frequency of rectangles: (Default 2) "))
        shapeSeed.append(temp)
        temp = eval(input("Relative frequency of ovals: (Default 2) "))
        shapeSeed.append(temp)
        temp = eval(input("Relative frequency of octogons: (Default 1) "))
        shapeSeed.append(temp)
    theIn = input("Would you like to use the standard size preset? ")
    if theIn[0] == "y" or theIn[0] == "Y":
        sizeSeed = SIZE_SEED
    else:
        temp = eval(input("Room length minimum: (Default 30) "))
        sizeSeed.append(temp)
        temp = eval(input("Room length range: (Default 120) "))
        sizeSeed.append(temp)
        temp = eval(input("Room width minimum: (Default 30) "))
        sizeSeed.append(temp)
        temp = eval(input("Room width range: (Default 120) "))
        sizeSeed.append(temp)
        temp = eval(input("Corridor short side length: (Default 30) "))
        sizeSeed.append(temp)
        temp = eval(input("Corridor long side minimum: (Default 150) "))
        sizeSeed.append(temp)
        temp = eval(input("Corridor long side range: (Default 100) "))
        sizeSeed.append(temp)
    return [poolSeed,shapeSeed,sizeSeed]

def printPresets():
    print("Here is a list of presets:")
    for preset in PRESET_NAMES:
        print("  ",preset)

def getSeed():
    """Asks the user what 'seed' they want to use"""
    print("Would you like to use the standard seed")
    standard = input("for dungeon generation? ")
    if standard[0] == "y" or standard[0] == "Y":
        return SEED_LIST
    else:
        print("Hit p to enter a preset, anything else to")
        custom = input("get a customized dungeon: ")
        if custom[0] == "p" or custom[0] == "P":
            printPresets()
            preset = input("Enter a valid preset: ")
            return eval(preset)
        else:
            return getCustomSeed()

def textMain():
    printIntro()
    wantMore = True
    while wantMore:
        n = input("How many dungeons to generate? (10) ")
        a = input("How many attempts to make each room? (3) ")
        if n == "":
            n = 10
        else:
            n = eval(n)
        if a == "":
            a = 3
        else:
            a = eval(a)
        seed = getSeed()
        stats = input("Do you want to collect stats istead? ")
        if stats[0] == "y" or stats[0] == "Y":
            s = input("Do you want the program to show its progress? ")
            if s[0] == "y" or s[0] == "Y":
                s = True
            else:
                s = False
            collectStats(n,a,s,seed)
        else:
            p = input("How long to pause btw dungeons? (0) ")
            if p == "":
                p = 0
            else:
                p = eval(p)
            main(n,a,p,seed)
        more = input("Do you want to make more dungeons? ")
        if more[0] != "y" and more[0] != "Y":
            wantMore = False
    
    

def myTest(door):
	myWin = GraphWin("Test",500,500)
	start = Room(200,200,300,300,"rectangle",["N","S","E","W"],myWin)
	start.draw()
	newRoom = createRandRoom(start,door)
	newRoom.draw()
	return [myWin,start,newRoom] 

def guiMain(): # WIP
    gui = GraphWin("Dungeon Generator "+VERSION,500,500)
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
    gui = GraphWin("Dungeon Generator "+VERSION,500,500)
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


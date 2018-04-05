import random
possExits = ["n","e","s","w"]
Rooms = []

def wantedExits (x,y, fromdir, xMax, yMax):
   wEx  = []
   if fromdir == "w":
     wEx.append("e")
   if fromdir == "e":
     wEx.append("w")
   if fromdir == "s":
     wEx.append("n")
   if fromdir == "n":
     wEx.append("s")
   myPosE = ["n","e","s","w"]
   nPosExits = 4
   if x == 0:
      myPosE.remove("w")
      nPosExits = nPosExits - 1
   if y == 0:
      myPosE.remove("s")
      nPosExits = nPosExits - 1
   if x == xMax:
      myPosE.remove("e")
      nPosExits = nPosExits - 1
   if y == yMax:
      myPosE.remove("n")
      nPosExits = nPosExits - 1
   randN = random.random()
   if randN < 0.10:
      nExits = 1
   elif randN < 0.42:
      nExits = 2
   elif randN < 0.75:
      nExits = 3
   else:
      nExits = 4
   nExits = min(nExits,nPosExits)
   while len(wEx) < nExits:
      e = random.choice(myPosE)
      if not e in wEx:
         wEx.append(e)
   return wEx

def createRoom (x, y, prevRoom, xMax,yMax):
   prevX = prevRoom[0]
   prevY = prevRoom[1]
   fromdir = " "
   if x > prevX:
      fromdir = "e"
   if x < prevX:
      fromdir = "w"
   if y > prevY:
      fromdir = "n"
   if y < prevY:
      fromdir = "s"

   roomExs = wantedExits(x,y,fromdir,xMax,yMax)
   Rooms.append([x, y, roomExs])


def getRoom(x,y):
   for r in Rooms:
      if x == r[0] and y == r[1]:
         return r
   return None

def printRooms(xMax,yMax):
   print("kj")
   for y in range(yMax-1,-1,-1):
      utstr = ""
      for x in range(0,xMax):
         r = getRoom(x,y)
         if r:
            utstr = utstr + "x"
         else:
            utstr = utstr + " "
      print(utstr)


def mazeGen(xMax, yMax):
   Rooms = []
   for y in range(0,yMax):
      for x in range(0,xMax):
         if x == 0 and y == 0:
            createRoom(x,y,[0,0,[]],xMax,yMax)
         elif x == 0:
            pRoom = getRoom(0, y-1)
            if pRoom and "n" in pRoom[2]:
               createRoom(x,y,pRoom,xMax,yMax)
         else:
            pRoom = getRoom(x-1,y)
            if pRoom and "e" in pRoom[2]:
               createRoom(x,y,pRoom,xMax,yMax)
mazeGen(5,5)
print(str(Rooms))
printRooms(5,5)
exit(0) 

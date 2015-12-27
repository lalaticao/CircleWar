#gamemap.py
from gameobject import *
from paramerror import *

class MapError(Exception):
    pass
class MapCheck(MapError):
    pass


class GameMap:
    _max = 6
    def __init__(self, **arg):
        if "file" in arg:
            self.load(arg["file"])
        else:
            self.empty()
            if "name" in arg:
                self.name=arg["name"]
            if "width" in arg:
                self.width=arg["width"]
            if "height" in arg:
                self.height=arg["height"]
    def empty(self):
        self.name = "New Map"
        self.width = 0
        self.height = 0
        self._bp = []
        self.obstacles = []
    def __str__(self):
        players=""
        for i in range(self.max_player()):
            players+="  (%d,%d)\n"%self._bp[i]
        obstacles=""
        for i in range(len(self.obstacles)):
            obstacles+="  (%d,%d) r=%d\n"%self.obstacles[i]
        return "[Circle War Map]\n" +\
               "name: "+self.name+"\n" +\
               "size: %dx%d\n"%(self.width,self.height) +\
               "players: \n"+players +\
               "obstacles: \n"+obstacles
    def copy(self):
        newmap = GameMap(name=self.name, width=self.width, height=self.height)
        for i in self._bp:
            newmap.addPlayer(*i)
        for i in self.obstacles:
            newmap.addObstacle(*i)
        return newmap
    
    def save(self):
        f=file(self.name+".cwmap","w")
        f.write("%d\n%d\n"%(self.width, self.height))
        f.write("%d\n"%self.max_player())
        for i in range(self.max_player()):
            f.write("%d\n%d\n"%self._bp[i])
        f.write("%d\n"%len(self.obstacles))
        for i in range(len(self.obstacles)):
            f.write("%d\n%d\n%d\n"%self.obstacles[i])
        f.close()
    def load(self, mapname):
        f=file(mapname+".cwmap")
        self.empty()
        self.name = mapname
        self.width=int(f.readline())
        self.height=int(f.readline())
        mp=int(f.readline())
        for i in range(mp):
            x=int(f.readline())
            y=int(f.readline())
            self.addPlayer(x,y)
        mo=int(f.readline())
        for i in range(mo):
            x=int(f.readline())
            y=int(f.readline())
            r=int(f.readline())
            self.addObstacle(x,y,r)

    
    def max_player(self):
        return len(self._bp)
    def addPlayer(self, x, y):
        if self.max_player() >= GameMap._max:
            raise MapError("there should be no more than %d players in a map"%GameMap._max)
        if (x,y) in self._bp:
            raise MapError("there is already a player at (%d,%d)"%(x,y))
        self._bp += [(x,y)]
    def removePlayer(self, x, y):
        if (x,y) not in self._bp:
            raise MapError("there is no player at (%d,%d)"%(x,y))
        self._hp.remove((x,y))
    def clearPlayer(self):
        self._bp=[]
    def getBornPoint(self, index):
        if index>=self.max_player() or index<0:
            raise ParamError("GameMap","getBornPoint","index",
                             "should be at least 0 and less than max_player(%d)"%self.max_player())
        return self._bp[index]
    
    def addObstacle(self, x, y, r):
        self.obstacles += [(x, y, r)]
    def delObstacle(self, (x,y,r)):
        if (x,y,r) in self.obstacles:
            self.obstacles.remove((x,y,r))
        
    def check(self):
        if self.width <= 0 or self.height <=0:
            raise MapCheck("width or height should be positive")
        if self.max_player() < 2:
            raise MapCheck("at least 2 players")
        for circle in self.obstacles:
            if not self.catch(circle[0],circle[1]):
                raise MapCheck("an obstacle is out of this map")

    def catch(self, x, y):
        return  x>=0 and x<=self.width and y>=0 and y<=self.height


def test():
    m = GameMap(name="test",width=10000,height=10000)
    m.addPlayer(0,0)
    m.addPlayer(10000,10000)
    m.addObstacle(5000,5000,500)
    m.save()
    print m
    m2 = GameMap(file="test")
    print m2

if __name__ == "__main__":
    test()

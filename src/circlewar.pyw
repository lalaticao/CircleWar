import sys

sys.path.append("import/base")
from graphics import *
from graphwinplus import *
from timer import *

sys.path.append("import")
from gamemap import *
import equipment
from gameobject import *
from camera import *
from controller import *

class CircleWar:
    def __init__(self, width, height, gamemap, *players):
        self._camera = Camera("Circle War !", width, height)
        
        self._ts = Timer(1)
        self._tf = Timer(1.0/30)

        self.loadMap(gamemap)
        for (bornplace, human, controller) in players:
            self.addPlayer(bornplace, human, controller)
        
    def loadMap(self, gamemap):
        gamemap.check()
        self._map = gamemap
        self.emptyPlayer()

    def emptyPlayer(self):
        self._human = []
        self._ctrl = []
        for i in range(self._map.max_player()):
            self._human += [[]]
            self._ctrl += [[]]
    def addPlayer(self, bornplace, human, controller):
        human.moveTo(*self._map.getBornPoint(bornplace))
        self._human[bornplace] += [human]
        self._ctrl[bornplace] += [controller]
        if self._camera.isRunning():
            self._camera.bindObject(human)

    def _doEveryFrame(self):
        #human run
        for b in range(len(self._human)):
            for i in range(len(self._human[b])):
                #weapon direction
                self._human[b][i].turnTo(self._ctrl[b][i].getDirection())
                #move
                self._human[b][i].run(self._ctrl[b][i].getMoveFourDirection())
                #set shoot state
                self._human[b][i].setShoot(self._ctrl[b][i].getShoot())
                #make bomb when shooting
                if self._human[b][i].isShooting():
                    self._bomb += [self._human[b][i].makeBomb(self._camera)]
                
                #can not go out of the bound
                if not self._map.catch(*self._human[b][i].center()):
                    if self._human[b][i].x < 0:
                        self._human[b][i].move(-self._human[b][i].x,0)
                    elif self._human[b][i].x > self._map.width:
                        self._human[b][i].move(self._map.width-self._human[b][i].x,0)
                    if self._human[b][i].y < 0:
                        self._human[b][i].move(0, -self._human[b][i].y)
                    elif self._human[b][i].y > self._map.height:
                        self._human[b][i].move(0, self._map.height-self._human[b][i].y)
                #can not go over the obstacle
                for obs in self._obstacle:
                    if obs.intersect(self._human[b][i]):
                        self._human[b][i].move(*obs.pushAway(self._human[b][i]))
        #bomb fly
        delbomblist = []
        for i in range(len(self._bomb)):
            mark = False #mark for removing it from the game
            #fly too far
            if not self._bomb[i].fly():
                mark = True
            #fly over the obstacle
            for obs in self._obstacle:
                if obs.intersect(self._bomb[i]):
                    mark = True
                    break
            #fly out of the map
            if not self._map.catch(*self._bomb[i].center()):
                mark = True
            #hit a human
            for h in self._human:
                for human in h:
                    if human.isAlive():
                        if human.team!=self._bomb[i].team:
                            if human.intersect(self._bomb[i]):
                                human.hurtBy(self._bomb[i])
                                mark=True
                                break
            if mark:
                delbomblist += [i]
        for i in range(len(delbomblist)):
            self._camera.unbindObject(self._bomb[delbomblist[i]-i])
            del self._bomb[delbomblist[i]-i]

        self._camera.refresh()
        
    def _doEveryTime(self):
        pass
    
    def start(self, lockplayer = None):
        self._obstacle = []
        for (x,y,r) in self._map.obstacles:
            self._obstacle+=[Obstacle(x,y,r)]
        
        self._bomb = []

        self._camera.startup(self._map.width, self._map.height)
        self._camera.bindObject(*self._obstacle)
        for b in range(len(self._human)):
            for i in range(len(self._human[b])):
                self._camera.bindObject(self._human[b][i])
        self._camera.lockObject(lockplayer)

        for ctrls in self._ctrl:
            for ctrl in ctrls:
                ctrl.start()
        self._ts.run()
        self._tf.run()
        self._fps = 0
        framecount = 0
        while True:
            if self._ts.check():
                self._fps=framecount
                framecount = 0
                self._camera.setTitle("Circle War ! fps:"+str(self._fps))
            if self._tf.check():
                framecount += 1
                self._doEveryFrame()
            self._doEveryTime()
            if self.isGameover():
                self.stop()
                break

    def isGameover(self):
        return False

    def stop(self):
        for ctrls in self._ctrl:
            for ctrl in ctrls:
                ctrl.stop()
        self._camera.stop()

def main():
    #map
    m = GameMap(file="test")
    """m = GameMap(name="test",width=1000,height=700)
    m.addPlayer(0,0)
    m.addPlayer(800,600)
    m.addPlayer(0,700)
    m.addPlayer(1000,0)
    for i in range(1,5):
        for j in range(1,4):
            m.addObstacle(i*200, j*200, 40)"""
    """m.addObstacle(200,140,1)
    m.addObstacle(800,140,1)
    m.addObstacle(800,560,1)
    m.addObstacle(200,560,1)
"""
    h1=Human(Team.Blue, equipment.LightWeapon)
    h2=Human(Team.Red , equipment.LightWeapon)
    game=CircleWar(800, 600, m)
    game.addPlayer(0, h1, KeyBoardAndMouseB(game))
    game.addPlayer(1, h2, RandomRobot(m.copy()))
    game.start(h1)
    
main()



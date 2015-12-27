#controller.py

class Controller:
    def __init__(self):
        pass
    def getShoot(self):
        pass #return "shoot" or "stop"
    def getDirection(self):
        pass #return (x,y) on Map
    def getMoveFourDirection(self):
        pass #return {"Up":(bool), "Down":(bool), "Left":(bool), "Right":(bool)}
    def start(self):
        pass
    def stop(self):
        pass
    def refresh(self):
        pass
    
class KeyBoardAndMouse(Controller):
    def __init__(self, game, movekey):
        Controller.__init__(self)
        self.camera = game._camera
        self.movekey = movekey
    def getShoot(self):
        return "shoot" if self.camera.isMouseLPressed() else "stop"
    def getDirection(self):
        p = self.camera.getMouseCurrentPoint()
        return self.camera.toMap(p.getX(),p.getY())
    def getMoveFourDirection(self):
        return {"Up":    self.camera.isKeyPressed([self.movekey["Up"]]),
                "Down":  self.camera.isKeyPressed([self.movekey["Down"]]),
                "Left":  self.camera.isKeyPressed([self.movekey["Left"]]),
                "Right": self.camera.isKeyPressed([self.movekey["Right"]])}
class KeyBoardAndMouseA(KeyBoardAndMouse):
    def __init__(self, game):
        KeyBoardAndMouse.__init__(self, game, {"Up":"Up",
                                               "Down":"Down",
                                               "Left":"Left",
                                               "Right":"Right"})
class KeyBoardAndMouseB(KeyBoardAndMouse):
    def __init__(self, game):
        KeyBoardAndMouse.__init__(self, game, {"Up":"w",
                                               "Down":"s",
                                               "Left":"a",
                                               "Right":"d"})
"""
class KeyBoard(Controller):
    def __init__(self, game, movekey, directionkey, shootkey):
        Controller.__init__(self)
        self.camera = game._camera
        self.movekey = movekey
        self.directionkey = directionkey
        self.shootkey = shootkey
        self.x, self.y = camera.width/2, camera.height/2
        self.v = 20
    def getShoot(self):
        return self.camera.isKeyPressed(shootkey)
    def getDirection(self):
        return self.camera.toMap(self.x, self.y)
    def getMoveFourDirection(self):
        return {"Up":    self.camera.isKeyPressed([self.movekey["Up"]]),
                "Down":  self.camera.isKeyPressed([self.movekey["Down"]]),
                "Left":  self.camera.isKeyPressed([self.movekey["Left"]]),
                "Right": self.camera.isKeyPressed([self.movekey["Right"]])}
    def refresh(self):
        dx, dy = 0, 0
        up    = self.camera.isKeyPressed([self.directionkey["Up"]])
        down  = self.camera.isKeyPressed([self.directionkey["Down"]])
        left  = self.camera.isKeyPressed([self.directionkey["Left"]])
        right = self.camera.isKeyPressed([self.directionkey["Right"]])
        if up and not down:
            dy = -self.v
        if down and not up:
            dy = self.v
        if left and not right:
            dx = -self.v
        if right and not left:
            dx = self.v
        if dx and dy:
            dx /= 2**0.5
            dy /= 2**0.5
        self.x += dx
        self.y += dy
        if self.x<0:self.x=0
        if self.x>self,camera.width:self.x=self.camera.width
        if self.y<0:self.y=0
        if self.y>self.camera.height:self.y=self.camera.height
class KeyBoardA(KeyBoard):
    def __init__(self, camera):
        KeyBoard.__init__(self, camera, {"Up":"w",
                                         "Down":"s",
                                         "Left":"a",
                                         "Right":"d"},
                                        {"Up":"t",
                                         "Down":"g",
                                         "Left":"f",
                                         "Right":"h"},
                                         "Alt")
class KeyBoardB(KeyBoard):
    def __init__(self, camera):
        KeyBoard.__init__(self, camera, {"Up":"i",
                                         "Down":"k",
                                         "Left":"j",
                                         "Right":"l"},
                                        {"Up":"Up",
                                         "Down":"Down",
                                         "Left":"Left",
                                         "Right":"Right"},
                                         "Control")
"""

    
import random
import sys
sys.path.append("base")
import timer

def _randomTrueOrFalse():
    return bool(random.randint(0,1))

class AI(Controller):
    def __init__(self, mapcopy):
        Controller.__init__(self)
        self.map = mapcopy
        
class RandomRobot(AI):
    def __init__(self, mapcopy):
        AI.__init__(self, mapcopy)
        self.t=timer.Timer(1)
        self.t2=timer.Timer(0.5)
        self.t.run()
        self.t2.run()
        self.fd={"Up":False,"Down":False,"Right":False,"Left":False}
        self.d=(0,0)
    def getShoot(self):
        return "shoot" if _randomTrueOrFalse() else "stop"
    def getDirection(self):
        if self.t2.check():
            self.d=(random.randint(0,self.map.width),
                    random.randint(0,self.map.height))
        return self.d
    def getMoveFourDirection(self):
        if self.t.check():
            self.fd = {"Up":   _randomTrueOrFalse(),
                       "Down": _randomTrueOrFalse(),
                       "Left": _randomTrueOrFalse(),
                       "Right":_randomTrueOrFalse()}
        return self.fd


    

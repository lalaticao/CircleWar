#camera.py
from paramerror import *
class CameraError(Exception):
    pass

import sys
sys.path.append("base")
from graphics import *
from graphwinplus import *


class Camera(GraphWinPlus):
    def __init__(self, title="Camera", width=800, height=600):
        if width < 800 or height < 600:
            raise ParamError("Camera","__init__","size",
                             "should be at least 800x600")
        
        GraphWinPlus.__init__(self, title, width, height)
        self.setBackground("gray")
        
        self._start = False
        self._objs = []
        self._x, self._y = 0, 0

    def isRunning(self):
        return self._start
    def startup(self, map_width, map_height, bind_objs=[], lock_obj=None):
        if self._start:
            raise CameraError("the camera has already startuped.")
        self._start = True
        self._mapw, self._maph = map_width, map_height

        self._back = Rectangle(Point(-20,-20),Point(self.width+20,
                                                    self.height+20))
        self._back.setOutline("Yellow")
        self._back.setWidth(10)
        self._back.draw(self)
        
        self.bindObject(*bind_objs)
        
        if lock_obj:
            self.lockObject(lock_obj)
        else:
            self._lock=None
            self.MoveCenterTo(self.width/2, self.height/2)
            
        self.refresh()
        
    def bindObject(self, *objs):
        if not self._start:
            raise CameraError("can't bind object before the camera startups.")
        for obj in objs:
            if obj not in self._objs:
                obj.draw(self)
                self._objs+=[obj]
                
    def unbindObject(self, *objs):
        if not self._start:
            raise CameraError("can't unbind object before the camera startups.")
        for obj in objs:
            if obj in self._objs:
                obj.undraw()
                self._objs.remove(obj)

    def lockObject(self, lock_obj):
        if not self._start:
            raise CameraError("can't lock object before the camera startups.")
        if lock_obj not in self._objs:
            raise CameraError("can't lock objects unbound to the camera.")
        self._lock = lock_obj
        self.MoveCenterTo(*lock_obj.center())

    def unlock(self):
        if not self._start:
            raise CameraError("can't lock object before the camera startups.")
        self._lock = None

    def objectLocked(self):
        return self._lock
    
    def stop(self):
        self._start = False
        for obj in self._objs:
            obj.undraw()
        self._objs = []
        self._back.undraw()

    def refresh(self):
        if self._start:
            if self._lock != None:
                x, y = self.toCamera(*self._lock.center())
                if   x < self.width/3:    self.Move(x - self.width/3, 0)
                elif x > self.width*2/3:  self.Move(x - self.width*2/3, 0)
                if   y < self.height/3:   self.Move(0, y - self.height/3)
                elif y > self.height*2/3: self.Move(0, y - self.height*2/3)

            for obj in self._objs:
                obj.graph.adjust(self)
                if self.catch(obj) or self.catch(obj.graph):
                    obj.refreshGraph(self)
            
    def catch(self, circle):
        x, y = self.toCamera(*circle.center())
        r = circle.r
        if x+r < 0 or x-r > self.width or y+r < 0 or y-r > self.height:
            return False
        if (x<0 or x>self.width) and (y<0 or y>self.height):
            dx = -x if x<0 else x-self.width
            dy = -y if y<0 else y-self.height
            if dx*dx + dy*dy > r*r:
                return False
        return True

    def toCamera(self, x, y):
        if not self._start:
            raise CameraError("can't lock object before the camera startups.")
        return (x-self._x, y-self._y)
    def toMap(self, x, y):
        if not self._start:
            raise CameraError("can't lock object before the camera startups.")
        return (x+self._x, y+self._y)

    def Move(self, dx, dy):
        if not self._start:
            raise CameraError("can't lock object before the camera startups.")
        self._x+=dx
        self._y+=dy
        x, y = self.getCenter()
        if x>self._mapw:
            self._x = self._mapw-self.width/2
        if x<0:
            self._x = 0-self.width/2
        if y>self._maph:
            self._y = self._maph-self.height/2
        if y<0:
            self._y = 0-self.height/2

        x, y = self._back.getP1().getX()+20, self._back.getP1().getY()+20
        if self._x<0:
            self._back.move(-self._x - x,0)
        elif self._x+self.width>self._mapw:
            self._back.move(self._mapw-self._x-self.width-x,0)
        else:
            self._back.move(-x,0)
        if self._y<0:
            self._back.move(0,-self._y - y)
        elif self._y+self.height>self._maph:
            self._back.move(0,self._maph-self._y-self.height-y)
        else:
            self._back.move(0,-y)
            
    def getCenter(self):
        if not self._start:
            raise CameraError("can't lock object before the camera startups.")
        return (self._x+self.width/2, self._y+self.height/2)
    def getLeftTop(self):
        if not self._start:
            raise CameraError("can't lock object before the camera startups.")
        return (self._x, self._y)
    
    def MoveTo(self, x, y):
        self.Move(*self.toCamera(x, y))
    def MoveCenterTo(self, x, y):
        if not self._start:
            raise CameraError("can't lock object before the camera startups.")
        self.Move(x-self._x-self.width/2, y-self._y-self.height/2)

        

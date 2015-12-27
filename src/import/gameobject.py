#gameobject.py
import random
from paramerror import *

import equipment

import sys
sys.path.append("base")
import graphics
import timer
import arc

import random

class _Team:
    def __init__(self, name, color):
        self.name = name
        self.color = color
    def __str__(self):
        return self.name
    
class Team:
    Red = _Team("Red","red")
    Blue = _Team("Blue","blue")
    Neutral = _Team("Neutral","white")
    All = (Red, Blue, Neutral)

def distanceOf((x1,y1),(x2,y2)):
    return float((x1-x2)**2+(y1-y2)**2)**0.5

class Circle:
    def __init__(self, x, y, r):
        self.x=x
        self.y=y
        if r<=0:
            raise ParamError("Circle","__init__","r",
                             "should be positive")
        self.r=r
    def center(self):
        return (self.x, self.y)
    def move(self, dx, dy):
        self.x+=dx
        self.y+=dy
    def moveTo(self, x, y):
        self.move(x-self.x, y-self.y)

    def intersect(self, other):
        return distanceOf(self.center(),other.center()) < self.r+other.r

class Graph(Circle):
    def __init__(self, x, y, r, color):
        Circle.__init__(self, x, y, r)
        self.c = graphics.Circle(graphics.Point(-1000,-1000), r)
        self.c.setWidth(3)
        self.c.setFill(color)
    def changeColor(self,color):
        self.c.setFill(color)
    def adjust(self, camera):
        x, y = self.c.getCenter().getX(), self.c.getCenter().getY()
        self.x, self.y = camera.toMap(x, y)
    def draw(self, camera):
        self.adjust(camera)
        self.c.draw(camera)
    def undraw(self):
        self.c.undraw()
    def move(self, dx, dy):
        Circle.move(self, dx, dy)
        self.c.move(dx, dy)
class HPBar(Circle):
    def __init__(self, x, y, r, layer=1, percentage=1):
        Circle.__init__(self, x, y, r)
        self.a = arc.CircleArc(graphics.Point(-1000,-1000), r-3, 90)
        self.a.setWidth(6)
        self.a.setOutline("green")
        self.t = graphics.Text(graphics.Point(-1000,-1000),layer)
        self.t.setFill("green")
        self.t.setStyle("bold")
        self.t.setSize(20)
        self.setPercentage(percentage)
    def adjust(self, camera):
        x, y = self.a.getCenter().getX(), self.a.getCenter().getY()
        self.x, self.y = camera.toMap(x, y)
    def draw(self, camera):
        self.adjust(camera)
        self.a.draw(camera)
        self.t.draw(camera)
    def undraw(self):
        self.a.undraw()
        self.t.undraw()
    def move(self, dx, dy):
        Circle.move(self, dx, dy)
        self.a.move(dx, dy)
        self.t.move(dx, dy)
    def setPercentage(self, percentage):
        self.a.setExtent(percentage*360 if 0<=percentage<1 else 359.999)
    def setLayer(self, layer):
        self.t.setText(layer)

class GameObject(Circle):
    def __init__(self, x, y, r, team, speed):
        Circle.__init__(self, x, y, r)
        
        if team not in Team.All:
            raise ParamError("GameObject","__init__","team",
                             "should be chosen from "+str(Team.All))
        self.team = team
        if speed < 0 :
            raise ParamError("GameObject","__init__","speed",
                             "can't be negative")
        self.v = speed
        self.graph = Graph(x, y, r, team.color)
        
        self._destroy = False
    def speed(self):
        return self.v
        
    def refreshGraph(self, camera):
        self.graph.adjust(camera)
        self.graph.moveTo(self.x, self.y)
    def draw(self, camera):
        self.graph.draw(camera)
    def undraw(self):
        self.graph.undraw()
        
class Bomb(GameObject):
    def __init__(self, x, y, d, dis, r, v, attack, team):
        GameObject.__init__(self, x, y, r, team, v)
        self._sx, self._sy = x, y
        self.attack = attack
        self._dis = dis
        d=list(d)
        k = float((d[0]-x)**2+(d[1]-y)**2)**0.5
        while k==0:
            d[0]=x+random.randint(-100,100)
            d[1]=y+random.randint(-100,100)
            k = float((d[0]-x)**2+(d[1]-y)**2)**0.5
        self._px = (d[0]-x)/k
        self._py = (d[1]-y)/k
        self._movetime=0
        
    def fly(self):
        self._movetime+=1
        d = self._movetime*self.v
        self.moveTo(int(self._px*d)+self._sx, int(self._py*d)+self._sy)
        return d<=self._dis
        
class LightBomb(Bomb):
    def __init__(self, x, y, d, team):
        Bomb.__init__(self, x, y, d, 500, 15, 15, 60, team)
class HeavyBomb(Bomb):
    def __init__(self, x, y, d, team):
        Bomb.__init__(self, x, y, d, 300, 60, 15, 100, team)
class SnipeBomb(Bomb):
    def __init__(self, x, y, d, team):
        Bomb.__init__(self, x, y, d, 100000, 5, 25, 500, team)
        
class Crisp(GameObject):
    def __init__(self, team, x, y, r, base_speed, *armor_classes):
        GameObject.__init__(self, x, y, r, team, base_speed)
        self.armor = []
        self.addArmor(*armor_classes)
    def speed(self):
        v = GameObject.speed(self)
        for armor in self.armor:
            v -= armor.weight()
        return v if v >= 0 else 0
    def defense(self):
        d=0
        for armor in self.armor:
            d+=armor.defense()
        return d
    
    def hpOut(self):
        return self.armor[-1].hp()
    def layer(self):
        return len(self.armor)
    def addArmor(self, *armor_class):
        for ac in armor_class:
            self.armor += [ac()]
        if self.layer()>0 and self._destroy:
            self.graph.changeColor(self.team.color)
            self._destroy = False
    
    def hurtBy(self, bomb):
        if not self._destroy:
            damage = bomb.attack - self.defense()
            self.armor[-1].subHP(damage)
            if self.armor[-1].hp() <= 0:
                del self.armor[-1]
            if self.layer() <= 0:
                self.destroy()
    def destroy(self):
        self._destroy = True
        self.graph.changeColor("")
    def isDestroyed(self):
        return self._destroy
    
class Obstacle(Crisp):
    def __init__(self, x, y, r):
        Crisp.__init__(self, Team.Neutral, x, y, r, 0, equipment.Obstacle)
    def pushAway(self, other):
        d = distanceOf(self.center(),other.center())
        x, y = other.center()
        while d==0 or d >= self.r+other.r:
            x=random.randint(1,self.x+self.r)
            y=random.randint(1,self.y+self.r)
            d=distanceOf(self.center(),(x,y))
        moved = self.r+other.r-d
        return (x-self.x)/d*moved, (y-self.y)/d*moved

class Life(Crisp):
    def __init__(self, team, x, y, r, d, base_speed, weapon_class, *armor_classes):
        Crisp.__init__(self, team, x, y, r, base_speed, *armor_classes)
        self.weapon = weapon_class()
        
        self._tshoot=timer.Timer(self.weapon.shoot())
        self._tshoot.run()
        self._shooting=False
        
        self.hpbar = HPBar(x, y, r)
        
        self.d=d
        self.l=graphics.Line(graphics.Point(0,0),graphics.Point(0,0))
        
    def speed(self):
        v = Crisp.speed(self) - self.weapon.weight()
        return v if v >= 0 else 0
    def draw(self, camera):
        Crisp.draw(self, camera)
        self.hpbar.draw(camera)
    def undraw(self):
        Crisp.undraw(self)
        self.hpbar.undraw()
        
    def _pind(self):
        try:
            k=float(self.r)/((self.d[0]-self.x)**2+(self.d[1]-self.y)**2)**0.5
        except ZeroDivisionError:
            k=0
        newx=int((self.d[0]-self.x)*k)+self.x
        newy=int((self.d[1]-self.y)*k)+self.y
        return newx, newy
    def refreshGraph(self, camera):
        Crisp.refreshGraph(self, camera)
        self.hpbar.adjust(camera)
        self.hpbar.moveTo(self.x,self.y)
        
        self.l.undraw()
        self.l = graphics.Line(graphics.Point(*camera.toCamera(self.x,self.y)),
                               graphics.Point(*camera.toCamera(*self._pind())))
        self.l.setArrow("last")
        self.l.setWidth(self.weapon.width())
        self.l.setFill(self.weapon.color())
        self.l.draw(camera)
        self.refreshHPBar()
    def refreshHPBar(self):
        try:
            self.hpbar.setPercentage(
                int(float(self.armor[-1].hp())/self.armor[-1].max_hp()*100)/100.0)
            self.hpbar.setLayer(self.layer())
        except:
            self.hpbar.setPercentage(0)
            self.hpbar.setLayer("")
            
    def hurtBy(self, bomb):
        Crisp.hurtBy(self, bomb)
        self.refreshHPBar()
    
    def isShooting(self):
        return self.isAlive() and self._shooting and self._tshoot.check()
    def setShoot(self, shoot):
        self._shooting = (shoot=="shoot")
        
    def makeBomb(self, camera):
        bomb=self.weapon.makeBomb(self.x, self.y, self.d, self.team)
        camera.bindObject(bomb)
        return bomb

    def turnTo(self, d):
        if self.isAlive():
            self.d=d
    def run(self, fourdirection):
        if self.isAlive():
            dx, dy = 0, 0
            if fourdirection["Up"] and not fourdirection["Down"]:
                dy -= self.speed()
            elif fourdirection["Down"] and not fourdirection["Up"]:
                dy += self.speed()
            if fourdirection["Left"] and not fourdirection["Right"]:
                dx -= self.speed()
            elif fourdirection["Right"] and not fourdirection["Left"]:
                dx += self.speed()
            if dx and dy:
                dx /= 2**0.5
                dy /= 2**0.5
            self.move(int(dx), int(dy))
    
    def isAlive(self):
        return not self.isDestroyed()
    
class Human(Life):
    def __init__(self, team, weapon_class, armor_class=None, point=(0,0), d=(0,0)):
        if armor_class:
            Life.__init__(self, team, point[0], point[1], 30, d, 10,weapon_class,equipment.Human,armor_class)
        else:
            Life.__init__(self, team, point[0], point[1], 30, d, 10,weapon_class,equipment.Human)


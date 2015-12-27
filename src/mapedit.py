#mapedit.py

import sys
sys.path.append("import")
sys.path.append("import/base")

from gamemap import *
from graphwinplus import *
from graphics import *
from arc import *
from textplus import *

class Menu:
    r_out = 50
    r_in  = 10
    def __init__(self, x, y, items):
        self.x, self.y = x, y
        self.items = items[:4]
        
        self.fillC = CircleArc(Point(x,y), Menu.r_out, 135, 0)
        self.outC = CircleArc(Point(x,y), Menu.r_out, 135, 0)
        self.inC  = CircleArc(Point(x,y), Menu.r_in, 135, 0)
        self.l = []
        for (dx, dy) in ((1,-1),(1,1),(-1,1),(-1,-1)):
            self.l += [Line( Point(x+dx*Menu.r_in/(2**0.5),
                                   y+dy*Menu.r_in/(2**0.5)),
                             Point(x+dx*Menu.r_out/(2**0.5),
                                   y+dy*Menu.r_out/(2**0.5)))]
        self.arc = [CircleArc(Point(x,y), Menu.r_out-5, 135, -90),
                    CircleArc(Point(x,y), Menu.r_out-5, 45, -90),
                    CircleArc(Point(x,y), Menu.r_out-5, -45, -90),
                    CircleArc(Point(x,y), Menu.r_out-5, -135, -90)]
        self.t=[]
        for (i, dx, dy) in ((0, 0,-1),(1, 1,0),(2, 0,1),(3, -1,0)):
            self.t += [Text(Point(x+dx*(Menu.r_out+Menu.r_in)/2,
                                  y+dy*(Menu.r_out+Menu.r_in)/2),
                            self.items[i])]

        self.fillC.setStyle(Arc.PIESLICE)
        self.fillC.setFill("white")
        self.fillC.setOutline("")
        self.outC.setOutline("purple")
        self.outC.setWidth(3)
        self.inC.setOutline("purple")
        self.inC.setWidth(3)
        for arc in self.arc:
            arc.setOutline("purple")
            arc.setWidth(10)
        for l in self.l:
            l.setOutline("purple")
            l.setWidth(2)
        
    def _dir(self, x, y):
        dx, dy = x-self.x, self.y-y
        d2 = dx**2 + dy**2
        if d2 >= Menu.r_in**2:
            if dy > -dx and dy >= dx:
                return 0
            if dy < dx and dy >= -dx:
                return 1
            if dy < -dx and dy <= dx:
                return 2
            if dy > dx and dy <= -dx:
                return 3
    def _point(self, x, y):
        d2 = (x-self.x)**2 + (y-self.y)**2
        if d2 <= Menu.r_out**2:
            return self._dir(x, y)
    def choose(self, win, mousekey):
        self.fillC.draw(win)
        self.outC.draw(win)
        self.inC.draw(win)
        pressed = True
        lasthover = None
        rsl = None
        i = 0
        while not win.isClosed():
            if i <= 360:
                self.fillC.setExtent(-i)
                self.outC.setExtent(-i)
                self.inC.setExtent(-i)
                if i>0 and (i-90)%90 == 0:
                    self.l[(i-90)/90].draw(win)
                if (i-45)%90 == 0:
                    self.t[(i-45)/90].draw(win)
                i += 5
            if pressed and not win.isMousePressed(set([mousekey])):
                p = win.getMouseCurrentPoint()
                rsl = self._dir(p.x, p.y)
                if rsl != None:
                    break
                pressed = False
            if not pressed:
                try:
                    p = win.checkMouse()[2]
                    rsl = self._point(p.x, p.y)
                    break
                except:pass
            p = win.getMouseCurrentPoint()
            if pressed:
                hover = self._dir(p.x, p.y)
            else:
                hover = self._point(p.x, p.y)
            if hover != lasthover:
                if lasthover != None:
                    self.arc[lasthover].undraw()
                if hover != None:
                    self.arc[hover].draw(win)
                lasthover = hover
        
        self.fillC.undraw()
        self.outC.undraw()
        self.inC.undraw()
        for arc in self.arc:
            arc.undraw()
        for l in self.l:
            l.undraw()
        for t in self.t:
            t.undraw()
        return rsl

class Slider:
    w = 6
    h = 15
    def __init__(self, x, y, length, minn, maxn, init_value = None):
        if init_value == None:
            init_value = minn
        self.x, self.y= x, y
        self.l = length-Slider.w/2
        if minn >= maxn:
            raise Exception()
        self.minn, self.maxn = minn, maxn
        
        self.line = Line(Point(x,  y+Slider.h/2), Point(x+length, y+Slider.h/2))
        self.line.setWidth(3)
        self.line.setFill("gray")
        self.rect = Rectangle(Point(0,0), Point(Slider.w, Slider.h))
        self.rect.setOutline("")
        self.rect.setFill("black")

        self.text = Text(Point(0,0), "")
        self.text.setTextColor("black")
        
        self.setValue(init_value)
    def draw(self, win):
        self.line.draw(win)
        self.rect.draw(win)
    def undraw(self):
        self.line.undraw()
        self.rect.undraw()
    
    def getValue(self):
        return self.v
    def setValue(self, value):
        if value > self.maxn:
            value = self.maxn
        elif value < self.minn:
            value = self.minn
        self.v = value
        x = (value-self.minn)*self.l/(self.maxn-self.minn)+self.x
        self.rect.move(x - self.rect.getP1().x,
                       self.y - self.rect.getP1().y)
        self.text.setText(value)
        self.text.move(x+Slider.w/2 - self.text.getAnchor().x,
                       self.y-7 - self.text.getAnchor().y)
    def moveTo(self, x):
        if x > self.x+self.l:
            x = self.x+self.l
        elif x < self.x:
            x = self.x
        self.setValue((x-self.x)*(self.maxn-self.minn)/self.l+self.minn)

    def isClickedOnRect(self, p):
        return 0 <= p.x-self.rect.getP1().getX() <= Slider.w \
           and self.y <= p.y <= self.y+Slider.h
    def isClickedOnLine(self, p):
        return self.x <= p.x <= self.x+self.l \
           and self.y <= p.y <= self.y+Slider.h \
           and not self.isClickedOnRect(p)
    def drag(self, mousekey, p, win):
        if self.isClickedOnRect(p):
            self.text.draw(win)
            while win.isMousePressed(set([mousekey])):
                p2 = win.getMouseCurrentPoint()
                if win.isKeyPressed(set(["Control"])):
                    if p2.x - p.x > 5:
                        self.setValue(self.getValue()+1)
                    elif p2.x - p.x < -5:
                        self.setValue(self.getValue()-1)
                    else: p2 = p
                else:
                    self.moveTo(p2.x)
                p = p2
            self.text.undraw()
        elif self.isClickedOnLine(p):
            self.text.draw(win)
            self.moveTo(p.x)
            while win.isMousePressed(set([mousekey])):pass
            self.text.undraw()

class Button:
    def __init__(self, x, y, w, h, text="", color="red", active=True):
        self.x, self.y, self.w, self.h =x, y, w, h
        self.color = color
        self.pressed = False
        self.visible = False
        self.active = active
        self.text = Text(Point(x+w/2, y+h/2), text)
        self.rect = Rectangle(Point(x,y), Point(x+w, y+h))
        self.rect.setWidth(4)
        self.rect.setFill("")
    def setTextSize(self, size):
        self.text.setSize(size)
    def getColor(self):
        return self.color
    def setColor(self, color):
        self.color = color
    def draw(self, win):
        self.visible = True
        self.rect.draw(win)
        self.text.draw(win)
    def undraw(self):
        self.visible = False
        self.text.undraw()
        self.rect.undraw()
    def isHovered(self, p):
        return 0<=p.x-self.x<=self.w and 0<=p.y-self.y<=self.h
    def hover(self, p):
        if self.visible:
            if self.active:
                self.text.setTextColor("black")
                self.rect.setOutline("black")
                if self.isHovered(p):
                    self.text.setStyle("bold")
                    if self.pressed:
                        self.rect.setFill(self.color)
                else:
                    self.text.setStyle("normal")
                    self.rect.setFill("")
            else:
                self.text.setStyle("normal")
                self.text.setTextColor("gray")
                self.rect.setFill("")
                self.rect.setOutline("gray")
    def isClicked(self, mousekey, p, win):
        if self.visible and self.active:
            if self.isHovered(p):
                self.pressed = True
                while win.isMousePressed(set([mousekey])):
                    self.hover(win.getMouseCurrentPoint())
                self.pressed = False
                p = win.getMouseCurrentPoint()
                self.hover(p)
                return self.isHovered(p)
        return False
class CircleButton(Button):
    def __init__(self, x, y, r, text="", color="red", active=True):
        Button.__init__(self, x-r, y-r, 2*r, 2*r, text, color, active)
        self.cx, self.cy, self.cr = x, y, r
        self.rect = Circle(Point(x,y), r)
        self.rect.setWidth(4)
        self.rect.setFill("")
    def isHovered(self, p):
        return (self.cx-p.x)**2+(self.cy-p.y)**2 <= self.cr**2

class EntryWin(GraphWin):
    def __init__(self, text = ""):
        GraphWin.__init__(self)
        
class Page:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.back = Rectangle(Point(x-5,y-5), Point(x+w+5,y+h+5))
        self.back.setFill("white")
        self.back.setOutline("")
        
    def show(self, win):
        self.back.draw(win)
    def hide(self):
        self.back.undraw()

class NewPage(Page):
    def __init__(self, x, y):
        Page.__init__(self, x-100, y-100, 200, 200)
        self.center = Point(x, y)
    def show(self, win):
        Page.show(self, win)
        try:
            b = CircleButton(self.x+100,self.y+100,20,"<=")
            b.draw(win)
            while True:
                b.hover(win.getMouseCurrentPoint())
                t = win.checkMouse()
                if t != None:
                    if b.isClicked(t[1],t[2],win):
                        b.setColor("blue" if b.getColor()=="red" else "red")
                        if t[1]=="R":
                            break
            b.undraw()
        except Exception,e:print e
        self.hide()
        
    def hide(self):
        Page.hide(self)

class OpenPage(Page):
    pass

class SettingPage(Page):
    pass

class MapEdit:
    max_width, max_height = 1100, 700
    min_width, min_height = 400, 400
    default_width, default_height = 600, 400
    settingfile = "mapedit.ini"
    
    def __init__(self, mapfile = ""):
        self.m = None
        if mapfile:
            try:self.m = GameMap(file = mapfile)
            except:pass

    def run(self):
        self.loadSettings()
        
        w = GraphWinPlus("Map Editor - %s" % \
                         ("Start" if self.m==None else self.m.name),
                         self.width, self.height)
        w.setMinSize(MapEdit.min_width,MapEdit.min_height)
        w.setMaxSize(MapEdit.max_width,MapEdit.max_height)
        w.setResizable(True, True)

        while not w.isClosed():
            try:
                #print w.isClosed()
                mousekey, p = w.checkMouse()[1:]
                mousewheel = w.checkMouseWheel()/120
                while mousewheel > 0:
                    pass
                    mousewheel -= 1
                while mousewheel < 0:
                    pass
                    mousewheel += 1
                if mousekey == "R":
                    rsl = Menu(p.x, p.y,
                           ["new","save","settings","load"]).choose(w,mousekey)
                    if rsl == 0:
                        m = NewPage(w.width/2, w.height/2).show(w)
                        if m != None:
                            self.m = m
                    elif rsl == 1:
                        print 1
                    elif rsl == 2:
                        print 2
                    elif rsl == 3:
                        print 3
                    else:
                        print "nothing"
                elif mousekey == "L":
                    if w.isKeyPressed(set(["Control"])):
                        pass
                    else:
                        pass
                
            except:pass
        w.close()

        
        self.width, self.height = w.width+4, w.height+4
        self.saveSettings()
    
    def saveSettings(self):
        f = file(MapEdit.settingfile, "w")
        f.write("#recent map file list:%d\n"%len(self.recent_list))
        for rf in self.recent_list:
            f.write(rf+"\n")
        f.write("#last size:%d:%d\n"%(self.width, self.height))
        f.write("#load last map:%s\n"%str(self.load_last_map))
        f.write("#create circle by:%s\n"%self.create_by)
        f.close()

    def loadSettings(self):
        try:
            f = file(MapEdit.settingfile, "r")
            
            fs = int(f.readline().split(":")[1])
            self.recent_list = []
            for i in range(fs):
                self.recent_list += [f.readline().split("\n")[0]]
                
            self.width, self.height = f.readline().split(":")[1:]
            self.width, self.height = int(self.width), int(self.height)
            if not (MapEdit.min_width<=self.width<=MapEdit.max_width
               and MapEdit.min_height<=self.height<=MapEdit.max_height):
                raise Exception("size error")
            
            self.load_last_map = (f.readline().split(":")[1] == "True")

            self.create_by = f.readline().split(":")[1]
            f.close()
        except:
            self.recent_list = []
            self.width = MapEdit.default_width
            self.height = MapEdit.default_height
            self.load_last_map = False
            self.create_by = "mouse"
            self.saveSettings()
    def addRecent(self, mapfile):
        while mapfile in self.recent_list:
            self.recent_list.remove(mapfile)
        self.recent_list += [mapfile]

    def checkRecent(self):
        removelist = []
        for f in self.recent_list:
            try:
                file(f).close()
            except:
                self.remove_list += [f]
        for f in removelist:
            while f in self.recent_list:
                self.recent_list.remove(f)
    def getRecent(self):
        self.checkRecent()
        self.recent_list = self.recent_list[:-21:-1]
        return self.recent_list




def main():
    MapEdit().run()
main()

#graphwinplus.py
"""
This module contains a class named GraphWinPlus which inheriting from GraphWin.
And it's a stronger version based on GraphWin as its name shows.

It supports changing the [icon], the [title] and the [size] of the window now!
It supports all [left], [right], and [mid] mousekey now!
It supports [keyboard] now!

I hope it will help with your final project. :-)

par Yannick (e-mail: shenxiaozhouxjzx@163.com)
"""
from graphics import *
class GraphWinPlus(GraphWin):
    """
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!OVERVIEW!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    Based on GraphWin. Use GraphWinPlus in the same way as GraphWin.
    Of course it expand the ability of GraphWin:
    1. There is more methods that can change the window or get information
       of the window.
    2. It expand the method getMouse to 9 new methods (the old method getMouse
       is reserved), they are getMouseAll, getMouseD, getMouseS,
       getMouseDL, getMouseL, getMouseDR, getMouseR, getMouseDM and getMouseM.
       The method checkMouse return more details now.
       It also add some new methods to get a set of mousekeys pressed and to
       tell a set of mousekeys whether are pressed.
    3. It supports keyboard now. The methods checkKey and getKey is similar
       to checkMouse and getMouse, the methods getKeyPressed and isKeyPressed
       is similar to getMousepressed and isMousePressed
    *the test at the end can be a simple guide to use this class
    
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!METHODS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    Following is new methods the class bringing:
    ***********************************************************************
    *Window Methods:  - change the window or get information of the window*
    ***********************************************************************
    # setTitle(title)
    # getTitle() -> str,  return the title of the window
      
    # setIcon(icon)  <icon>(str) is the path of the icon file(.ico, ...)
      
    # setSize(width, height) set the window to size of <width> x <height>
    # setWidth(width)
    # setHeight(height)
      
    # getWidth() -> int
    # getHeight() -> int
      
    # setResizable(rewidth=False,reheight=False)  if <rewidth> is True then
                        user can change the width of the window. if <reheight>
                        is True then user can change the height of the window
    # setMinSize(width,height)  set the minimum size of the window
    # setMaxSize(width,height)  set the maximum size of the window
    ***********************************************************************
    *Mouse Methods:  - make your mouse more useful                        *
    ***********************************************************************
    # getMousePressed() -> set,  return a set of mousekey pressed. The element
                        can be "L"(for left mouskey pressed), "R"(for right
                        mousekey pressed) and "M"(for mid mousekey pressed).
      - isMousePressed(X) -> bool,  return True when all elements in the set <X>
                        is pressed. For example, the calling statement
                        gwp.isMousePressed(set(["L","R"]))
                        will return True when the user pressed both left
                        mousekey and right mousekey (mid mouse key can be also
                        pressed).
      - isMouseLPressed() -> bool, return True when left mouse key is pressed
      - isMouseRPressed() -> bool, return True when right mouse key is pressed
      - isMouseMPressed() -> bool, return True when mid mouse key is pressed

    # getMouseCurrentPoint() -> Point,  return the point where the mouse now is

    # checkMouse() -> tuple(int, str, Point) or None,
                        return a tuple which contains the times mouse
                        clicked(1 or 2), which mouse is clicked("L", "R" or "M")
                        and the position in the window where mouse is clicked.
                        It will return immediately the tuple if mouse is first
                        clicked or is clicked after a call of checkMouse or
                        the methods related with getMouse, None otherwise.
                        *caution: call getMousePressed after a click won't
                        influence checkMouse
    # getMouseAll() -> tuple(int, str, Point),  return the same as checkMouse
                        but it won't return until mouse is clicked.
      - getMouseD() -> tuple(str, Point),  return mousekey clicked("L","R","M")
                        and the position where mouse clicked.
                        it will return only when mouse is double-clicked.
      ---- getMouseDL() -> Point,
                        return only when leftmousekey is double-clicked.
      ---- getMouseDR() -> Point,
                        return only when rightmousekey is double-clicked.
      ---- getMouseDM() -> Point,
                        return only when midmousekey is double-clicked.
      - getMouseS() -> tuple(str, Point),  return mousekey clicked("L","R","M")
                        and the position where mouse clicked.
                        it will return only when mouse is single-clicked.
      ---- getMouseL() -> Point,
                        return only when leftmousekey is single-clicked.
      ---- getMouseR() -> Point,
                        return only when rightmousekey is single-clicked.
      ---- getMouseM() -> Point,
                        return only when midmousekey is single-clicked.

    # checkMouseWheel() -> int,  similar to checkMouse, but return 0 instead
                        of None because mouse wheel is scolled by 0 which
                        has the same meaning as mouse wheel not scolled.
                        it return a interger in general a multiple of 120,
                        positive when wheel scolled forward and nagetive
                        when wheel scolled back.
    # getMouseWheel() -> int,  return the same as checkMouseWheel
                        but won't return until mouse wheel is scolled.
                        (so it won't return 0)
    ***********************************************************************  
    *Keyboard Methods:  - the most effective way to input or operate      *
    ***********************************************************************
    # getKeyPressed() -> set,  return a set of keys pressed.
                        For example, when the user is pressing (no releasing)
                        the keys 'ctrl' and 'A', the calling statement
                        gwp.getKeyPressed()
                        will return
                        set(["Control", "a"]).
      - isKeyPressed(X) -> bool,  if all elements in set <X> is pressed.
                        For example, the calling statement
                        gwp.isKeyPressed(set(["Shift", "Control", "a"]))
                        will return True when the user is pressing
                        (no releasing)the keys 'ctrl', 'shift' and 'A'.

    # checkKey() -> str or None, similar to checkMouse.
                        it will return immediately the name of the key
                        if the key is pressed the first time or
                        is pressed after the final call of checkKey and getKey.
                        it return None otherwise.
                        *caution: call getKeyPressed after a click won't
                        influence checkKey

    # getKey() -> str,  it won't return until a key is pressed.
    """
    
    def __init__(self, title="Graphics Window Plus", width=400, height=400):
        GraphWin.__init__(self, title, width, height, True)
        self.setSize(width, height)
        
        #Window init
        self._title=title
        self._bindWindowEvents()
        
        #Mouse init
        self._curX, self._curY = 0, 0
        self._mouseKey = None
        self._clickTimes = None
        self._mousePressed = set()
        self._mouseWheel = 0
        self._bindMouseEvents()

        #Keyboard init
        self._keyPressed = set()
        self._key = None
        self._bindKeyboardEvents()
        
    ##################################################################
    #Window Methods
        
    def _bindWindowEvents(self):
        self.master.bind("<Configure>",self._onConfigure)
    def _onConfigure(self,e):
        infostr = self.winfo_geometry().split("+")[0].split("x")
        self.width, self.height = [int(i) for i in infostr]
        self.config(width=self.width,height=self.height)

    def setTitle(self, title):
        """Set the title of the window to <title>."""
        self._title=title
        self.master.title(title)
    def getTitle(self):
        return self._title

    def setIcon(self, icon):
        self.master.iconbitmap(icon)

    def setSize(self,width,height):
        self.master.geometry(str(width)+"x"+str(height))
    def setWidth(self,width):
        self.master.geometry(str(width)+"x"+str(self.height))
    def setHeight(self,height):
        self.master.geometry(str(self.width)+"x"+str(height))
    
    def setResizable(self,rewidth=False,reheight=False):
        self.master.resizable(rewidth,reheight)
    def setMinSize(self,width,height):
        self.master.minsize(width,height)
    def setMaxSize(self,width,height):
        self.master.maxsize(width,height)
    
    ##################################################################
    #_Mouse private methods
    
    def _numToStr(self,num):
        return "L" if num==1 else ("M" if num==2 else "R")
    def _pressMouseX(self,key):
        self._mousePressed.add(key)
    def _bindMouseEvents(self):
        self.unbind("<Button-1>")
        
        self.bind("<Button-1>", self._onClick_X)
        self.bind("<Button-2>", self._onClick_X)
        self.bind("<Button-3>", self._onClick_X)
        
        self.bind("<Double-Button-1>",self._onDouble_X)
        self.bind("<Double-Button-2>",self._onDouble_X)
        self.bind("<Double-Button-3>",self._onDouble_X)
        
        self.bind("<Motion>",self._onMouseMove)
        self.bind("<B1-Motion>",self._onMouseMoveL)
        self.bind("<B2-Motion>",self._onMouseMoveM)
        self.bind("<B3-Motion>",self._onMouseMoveR)
        self.bind("<ButtonRelease>",self._onRelease)

        self.master.bind("<MouseWheel>",self._onMouseWheel)
        
    #Mouse Events Handler
    def _onClick_X(self, e):
        self._mouseKey = self._numToStr(e.num)
        self._clickTimes = 1
        self.mouseX = e.x
        self.mouseY = e.y
        self._pressMouseX(self._mouseKey)
    def _onDouble_X(self, e):
        self._mouseKey = self._numToStr(e.num)
        self._clickTimes = 2
        self.mouseX = e.x
        self.mouseY = e.y
        self._pressMouseX(self._mouseKey)
    def _onRelease(self,e):
        if self._numToStr(e.num) in self._mousePressed:
            self._mousePressed.remove(self._numToStr(e.num))
    def _onMouseMove(self,e):
        self._curX=e.x
        self._curY=e.y
        self._mousePressed = set()
    def _onMouseMoveL(self,e):
        self._onMouseMove(e)
        self._pressMouseX("L")
    def _onMouseMoveM(self,e):
        self._onMouseMove(e)
        self._pressMouseX("M")
    def _onMouseMoveR(self,e):
        self._onMouseMove(e)
        self._pressMouseX("R")
    def _onMouseWheel(self,e):
        self._mouseWheel = e.delta
    
    ##################################################################
    #Mouse Methods
        
    #getMousePressed
    def getMousePressed(self):
        if self.isClosed():
            raise GraphicsError("getMousePressed in closed window")
        self.update()
        return self._mousePressed
    def isMousePressed(self,X):
        mp=self.getMousePressed()
        for x in X:
            if not (x in mp):
                return False
        return True
    def isMouseLPressed(self):
        return "L" in self.getMousePressed()
    def isMouseRPressed(self):
        return "R" in self.getMousePressed()
    def isMouseMPressed(self):
        return "M" in self.getMousePressed()

    #getMouseCurrentPoint
    def getMouseCurrentPoint(self):
        return Point(self._curX,self._curY)

    #checkMouse
    def checkMouse(self):
        p=GraphWin.checkMouse(self)
        if p:
            return self._clickTimes, self._mouseKey, p
        return None
    
    #getMouseAll
    def _getMouse(self):
        self.mouseX = None
        self.mouseY = None
        while self.mouseX == None or self.mouseY == None:
            self.update()
            if self.isClosed(): raise GraphicsError("getMouse in closed window")
        x,y = self.toWorld(self.mouseX, self.mouseY)
        self.mouseX = None
        self.mouseY = None
        return Point(x,y)

    def getMouseAll(self):
        self._mouseKey = None
        self._clickTimes = None
        p=self._getMouse()
        return self._clickTimes, self._mouseKey, p
    
    def getMouseD(self):
        while True:
            t=self.getMouseAll()
            if t[0] == 2:
                return t[1], t[2]
    def getMouseDL(self):
        while True:
            t=self.getMouseD()
            if t[0] == "L":
                return t[1]
    def getMouseDR(self):
        while True:
            t=self.getMouseD()
            if t[0] == "R":
                return t[1]
    def getMouseDM(self):
        while True:
            t=self.getMouseD()
            if t[0] == "M":
                return t[1]

    def getMouseS(self):
        while True:
            t = self.getMouseAll()
            return t[1], t[2]
    def getMouse(self):
        return self.getMouseL()
    def getMouseL(self):
        while True:
            t=self.getMouseS()
            if t[0] == "L":
                return t[1]
    def getMouseR(self):
        while True:
            t=self.getMouseS()
            if t[0] == "R":
                return t[1]
    def getMouseM(self):
        while True:
            t=self.getMouseS()
            if t[0] == "M":
                return t[1]
            
    #checkMouseWheel
    def checkMouseWheel(self):
        if self.isClosed():
            raise GraphicsError("checkMouseWheel in closed window")
        self.update()
        if self._mouseWheel != 0:
            mw, self._mouseWheel = self._mouseWheel, 0
            return mw
        else:
            return 0

    #getMouseWheel
    def getMouseWheel(self):
        self._mouseWheel=0
        while self._mouseWheel == 0:
            self.update()
            if self.isClosed():
                raise GraphicsError("getMouseWheel in closed window")
        mw, self._mouseWheel = self._mouseWheel, 0
        return mw
            
    ##################################################################
    #_Keyboard private methods
    
    def _delTail(self,key):
        if ("_L" in key) or ("_R" in key):
            key=key[:-2]
        return key
    def _bindKeyboardEvents(self):
        self.master.bind("<KeyPress>",self._onKeyPress)
        self.master.bind("<KeyRelease>",self._onKeyRelease)
        
    #Keyboard Events Handler
    def _onKeyPress(self,e):
        self._keyPressed.add(self._delTail(e.keysym))
        self._key=self._delTail(e.keysym)
    def _onKeyRelease(self,e):
        if self._delTail(e.keysym) in self._keyPressed:
            self._keyPressed.remove(self._delTail(e.keysym))
            
    ##################################################################
    #Keyboard methods
            
    def getKeyPressed(self):
        if self.isClosed():
            raise GraphicsError("getKeyPressed in closed window")
        self.update()
        return self._keyPressed
    
    def isKeyPressed(self,X):
        kp=self.getKeyPressed()
        for x in X:
            if not (x in kp):
                return False
        return True
    
    def checkKey(self):
        if self.isClosed():
            raise GraphicsError("checkKey in closed window")
        self.update()
        if self._key != None:
            k, self._key = self._key, None
            return k
        else:
            return None
        
    def getKey(self):
        self._key = None
        while self._key == None:
            self.update()
            if self.isClosed(): raise GraphicsError("getKey in closed window")
        k, self._key = self._key, None
        return k

def test():
    w=GraphWinPlus("hi",1000,300)
    #window methods test
    w.setBackground("blue")
    #w.setIcon("icontest.ico") #icontest.ico should be a icon file
    w.setSize(800,200)
    input()
    w.setWidth(900)
    w.setHeight(400)
    w.setResizable(True,True)
    w.setMinSize(100,100)
    w.setMaxSize(1100,400)
    while True:
        w.setTitle(("(%d,%d)"+"""Test:getMouseWheel,  Scroll your mouse wheel.  
               (Finish by scrolling hard)""")%(w.getMouseCurrentPoint().getX(),
                                             w.getMouseCurrentPoint().getY()))
        m=w.getMouseWheel()
        print m
        if m>=360 or m<=-360:
            break
    while True:
        w.setTitle(("(%d,%d)"+"""Test:checkMouseWheel,  Scroll your mouse wheel
               (scrolling hard)""")%(w.getMouseCurrentPoint().getX(),
                                             w.getMouseCurrentPoint().getY()))
        m=w.checkMouseWheel()
        print m
        if m>=360 or m<=-360:
            break
    while True:
        w.setTitle(("(%d,%d)"+"""Test:getMouseAll,
                Click or double-clilck any mouse key  
               (press on three key)""")%(w.getMouseCurrentPoint().getX(),
                                             w.getMouseCurrentPoint().getY()))
        m=w.getMouseAll()
        print m
        if w.isMousePressed(set(["L","R","M"])):
            break
    while True:
        w.setTitle(("(%d,%d)"+"""Test:getKey,
            press any key  (press escape)""")%(w.getMouseCurrentPoint().getX(),
                                             w.getMouseCurrentPoint().getY()))
        k=w.getKey()
        print k
        if k=="Escape":
            break
    while True:
        w.setTitle(("(%d,%d)"+"""Test:getMousePressed,
                Click or double-clilck any mouse key  
               (press on three key)""")%(w.getMouseCurrentPoint().getX(),
                                             w.getMouseCurrentPoint().getY()))
        print w.getMousePressed()
        if w.isMousePressed(set(["L","R","M"])):
            break
    while True:
        w.setTitle(("(%d,%d)"+"""Test:getKeyPressed,
            press any key  (press escape)""")%(w.getMouseCurrentPoint().getX(),
                                             w.getMouseCurrentPoint().getY()))
        print w.getKeyPressed()
        if w.isKeyPressed(set(["Escape"])):
            break
    while True:
        w.setTitle(("(%d,%d)"+"""Test:checkMouse,
                Click or double-clilck any mouse key  
               (press on three key)""")%(w.getMouseCurrentPoint().getX(),
                                             w.getMouseCurrentPoint().getY()))
        m=w.checkMouse()
        if m:
            print m
        else:
            print "------"
        if w.isMousePressed(set(["L","R","M"])):
            break
    while True:
        w.setTitle(("(%d,%d)"+""""Test:checkKey,
            press any key  (press escape)""")%(w.getMouseCurrentPoint().getX(),
                                             w.getMouseCurrentPoint().getY()))
        k=w.checkKey()
        if k:
            print k
        else :
            print "Nothing is pressed."
        if k == "Escape":
            break
    w.close()
if __name__ == "__main__":
    test()

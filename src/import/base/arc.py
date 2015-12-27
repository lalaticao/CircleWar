from graphics import *
from graphics import _BBox

DEFAULT_CONFIG["style"]=tk.ARC
DEFAULT_CONFIG["start"]=0
DEFAULT_CONFIG["extent"]=360

#Arc in style of graphics
class Arc(_BBox):
    ARC = "arc"
    CHORD = "chord"
    PIESLICE = "pieslice"
    
    def __init__(self, p1, p2, start=0, extent=360):
        _BBox.__init__(self, p1, p2,
                       ["outline","width","fill","start","extent","style"])
        self.setStart(start)
        self.setExtent(extent)
        
    def clone(self):
        other = Arc(self.p1, self.p2)
        other.config = self.config.copy()
        return other
    
    def setStyle(self, style):
        self._reconfig("style", style)
    def setStart(self, start):
        self._reconfig("start", start)
    def setExtent(self, extent):
        if 0 <= 360 - extent <= 0.01:
            extent = 359.999
        if 0 <= extent + 360 <= 0.01:
            extent = -359.999
        self._reconfig("extent",extent)
        
    def _draw(self, canvas, options):
        p1 = self.p1
        p2 = self.p2
        x1,y1 = canvas.toScreen(p1.x,p1.y)
        x2,y2 = canvas.toScreen(p2.x,p2.y)
        return canvas.create_arc(x1,y1,x2,y2,options)

#CircleArc in style of graphics
class CircleArc(Arc):
    def __init__(self, center, radius, start=0, extent=360):
        p1 = Point(center.x-radius, center.y-radius)
        p2 = Point(center.x+radius, center.y+radius)
        Arc.__init__(self, p1, p2, start, extent)
        self.radius = radius
    def clone(self):
        other = CircleArc(self.getCenter(), self.radius)
        other.config = self.config.copy()
        return other
    def getRadius(self):
        return self.radius
        

#textplus.py

from graphics import *
DEFAULT_CONFIG["anchor"]="nw"
class TextPlus(Text):
    N,NE,E,SE,S,SW,W,NW,C="n","ne","e","se","s","sw","w","nw","center"
    L,R,F="left","right","fill"
    def __init__(self, p, text):
        GraphicsObject.__init__(self, ["fill","text","font","anchor"])
        self.setText(text)
        self.anchor = p.clone()
        self.setFill(DEFAULT_CONFIG['outline'])
        self.setOutline = self.setFill

    def setAnchorDir(self, anchor):
        self._reconfig("anchor", anchor)

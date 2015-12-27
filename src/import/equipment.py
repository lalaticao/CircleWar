#equipment.py
from paramerror import *

import gameobject

import sys
sys.path.append("base")
import graphics

class _Armor:
    def __init__(self, max_hp, defense, weight):
        self._mhp=max_hp
        self._hp=max_hp
        self._d=defense
        self._w=weight
    def max_hp(self):
        return self._mhp
    def hp(self):
        return self._hp
    def addHP(self, add):
        self._hp += add
        if self._hp > self._mhp:
            self._hp=self._mhp
    def subHP(self, sub):
        self._hp -= sub
        if self._hp<0:
            self._hp=0
    def defense(self):
        return self._d
    def weight(self):
        return self._w

class Obstacle(_Armor):
    def __init__(self):
        _Armor.__init__(self,1000000000000,100000000000,1000000000000)

class Human(_Armor):
    def __init__(self):
        _Armor.__init__(self, 100, 0, 0)
        
class LightArmor(_Armor):
    def __init__(self):
        _Armor.__init__(self, 100, 20, 1)
class NormalArmor(_Armor):
    def __init__(self):
        _Armor.__init__(self, 300, 50, 3)
class HeavyArmor(_Armor):
    def __init__(self):
        _Armor.__init__(self, 500, 80, 5)

class _Weapon:
    def __init__(self, bomb_class, weight, shoot, color, width):
        self._bc=bomb_class
        self._s=shoot
        self._w=weight
        self._c=color
        self._wid=width
    def weight(self):
        return self._w
    def shoot(self):
        return self._s
    def width(self):
        return self._wid
    def color(self):
        return self._c
    def makeBomb(self, x, y, d, team):
        return self._bc(x, y, d, team)

class LightWeapon(_Weapon):
    def __init__(self):
        _Weapon.__init__(self, gameobject.LightBomb, 0, 0.6, "yellow", 3)

class HeavyWeapon(_Weapon):
    def __init__(self):
        _Weapon.__init__(self, gameobject.HeavyBomb, 1, 1, "black", 6)

class Snipe(_Weapon):
    def __init__(self):
        _Weapon.__init__(self, gameobject.SnipeBomb, 3, 3, "green",9)


        

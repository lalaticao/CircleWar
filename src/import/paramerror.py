#paramerror.py

class ParamError(Exception):
    def __init__(self, classname, methodname, param, description):
        self.c=classname
        self.m=methodname
        self.p=param
        self.d=description
    def __str__(self):
        return self.c+"-"+self.m+": <"+self.p+"> "+self.d

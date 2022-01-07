import math 

__circuit__ = [(50,30),(20,100),(200, 150),(50, 300),(150,400),(40, 500),(220,520),(220, 260),(400,260),(300,410),(370, 540),(570,540),(600, 450),(450,50),(680,200)]
__screenSize__ = (720, 576)

# Utility functions for handling points
def vecDiff(v1,v2):
    return (v1[0]-v2[0],v1[1]-v2[1])
def vecAdd(v1,v2):
    return (v2[0]+v1[0],v2[1]+v1[1])
def vecScalarMult(v, s):
    return (v[0]*s, v[1]*s)
def vecDot(v1, v2):
    return v1[0]*v2[0]+v1[1]*v2[1];
def vecInter(scalar, v1, v2):
    return (v1[0]+scalar*(v2[0]-v1[0]), v1[1]+scalar*(v2[1]-v2[0]))
def approximateLength(v1):
    '''This should be rewritten with an approximate length function (approximating it with no sqrt calls)'''
    return math.sqrt(v1[0]**2+v1[1]**2)
def approximateDistance(v1,v2):
    return approximateLength(vecDiff(v1,v2))
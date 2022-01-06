import math 

### TODO
__circuit__ = ((10,10),(10,100),(100, 150),(120, 300),(46,424),(46, 524),(220,520),(220, 260),(300,260),(300,416),(370, 540),(470,540),(600, 450),(550,40),(680,200))
__screenSize__ = (720, 576)

# Utility functions for handling points
# I should probably build a class of vectors
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
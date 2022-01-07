import pygame
import math
import random

import utils

class Vehicule:
    _coords = (0,0)   # vector
    _speed = (2,4)    # vector 
    _speedLimit = (7, 25)
    _force = (0,0)  # acceleration
    _maxforce = 10
    _radius = 6
    _minradius = 6
    _maxradius = 20
    _seeInFuture = 3

    ### ADDED
    _hp = 100

    ### ADDED
    def _calculateMaxSpeed(self):
        return math.ceil(self._speedLimit[1] + (self._speedLimit[1] - self._speedLimit[0]) / (self._maxradius - self._minradius) * (self._minradius - self._radius))

    def __init__(self, coords=(0,0), speed=(1,1), force =(1,1), **kargs):
        self._coords = coords
        self._force = force
        self._radius = kargs.get("radius", 6)
        self._speed = speed
        self._color = (255, random.randint(0,255), random.randint(10,200))
        self._colorfg = tuple([int(c/2) for c in self._color])
        self._maxspeed = self._calculateMaxSpeed()

    def position(self): return self._coords

    def steerUpdate(self, track, vehicules):
        self._force = (0,0)
        self._force = utils.vecAdd(self._force, self.steerPathFollow(track))
        #steerSeparation(self, vehicules)

    def steerPathFollow(self, track):
        (s,p,l) = track._closestSegmentPointToPoint(self._coords)
        # TODO: We should first add a force if l is too large (too far from the middle of the track) 
        # This is the future position
        (sf, futurePosition) = track._segmentPointAddLength(s, p, max(10,utils.approximateLength(self._speed)) * self._seeInFuture) 
        # We just have to register a force to get to futurePosition !
        force = utils.vecDiff(futurePosition, self._coords)
        force = utils.vecScalarMult(force,self._maxforce/utils.approximateLength(force))
        return force

    def steerSeparation(self, vehicules):
        forceAccu = (0,0) # starts with a fresh force
        # for v in vehicules:
        #     if v is not self:


    def drawMe(self, screen):
        pygame.draw.circle(screen,self._color,   self._coords,self._radius,0)
        pygame.draw.circle(screen,self._colorfg, self._coords,self._radius,1)
    
    @staticmethod
    def handleCollisions(vehicules):
        " Simple collision checking. Vehicules get damaged"
        for i,v1 in enumerate(vehicules):
            for v2 in vehicules[i+1:]:
                offset = utils.vecDiff(v2._coords, v1._coords)
                al = utils.approximateLength(offset)
                if al != 0 and al < v1._radius + v2._radius - 1: # collision
                        v1._coords=(int(v1._coords[0]+offset[0]/al*(v1._radius+v2._radius)),
                                    int(v2._coords[1]+offset[1]/al*(v1._radius+v2._radius)))
                        ### ADDED to create damages to the vehicules
                        print("V1 hp's : {} | V2 hp's : {}".format(v1._hp, v2._hp))
                        v1._hp = v1._hp - round(abs(v2._force[0]))
                        v2._hp = v2._hp - round(abs(v1._force[0]))

        for i,v1 in enumerate(vehicules):
            if v1._hp <= 0:
                print("A vehicule has been deleted")
                vehicules.remove(v1)
    
    @staticmethod
    def updatePositions(vehicules):
        for v in vehicules:
            v._speed = utils.vecAdd(v._speed, v._force)
            l = utils.approximateLength(v._speed)
            if l > v._maxspeed:
                v._speed = utils.vecScalarMult(v._speed, v._maxspeed / l)
            v._coords= (v._coords[0]+int(v._speed[0]), v._coords[1]+int(v._speed[1]))

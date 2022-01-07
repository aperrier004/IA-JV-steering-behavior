import pygame
import random

import utils
from model.track     import Track
from model.vehicule  import Vehicule

class Scene:
    _track= None
    _vehicules = None
    _screen = None
    _font = None
    ### ADDED
    _vehiculeRadius = 6

    _mouseCoords = (0,0)

    def __init__(self, screenSize = utils.__screenSize__):
        pygame.init()
        self._screen = pygame.display.set_mode(screenSize)
        self._track = Track(self._screen)
        self._vehicules = []
        self._font = pygame.font.SysFont('Arial', 15)

    def drawMe(self):
        self._screen.fill((0,0,0))
        self._track.drawMe(scene = self)
        for vehicule in self._vehicules:
            vehicule.drawMe(self._screen)

        # Illustrate the closestSegmentPointToPoint function
        (s,p,l) = self._track._closestSegmentPointToPoint(self._mouseCoords)
        pygame.draw.line(self._screen, (128,255,128),p, self._mouseCoords)
        #print(self._track._segmentPointAddLength(s,p,150))
        pygame.draw.circle(self._screen, (128,255,128),self._track._segmentPointAddLength(s,p,150)[1],20,1)
        
        ### ADDED to draw the vehicule radius
        textToShow = "Vehicule's radius: {}".format(self._vehiculeRadius).encode()
        textSurface = self._font.render(textToShow, False, (255,255,255))
        self._screen.blit(textSurface, (utils.__screenSize__[0]-120, utils.__screenSize__[1] - utils.__screenSize__[1] + 10))

        textToShow = "Use mouse's wheel to control vehicule's radius".encode()
        textSurface = self._font.render(textToShow, False, (255,255,255))
        self._screen.blit(textSurface, (utils.__screenSize__[0]-258, utils.__screenSize__[1] - utils.__screenSize__[1] + 25))
        ###

        pygame.display.flip()

    def drawText(self, text, position, color = (255,128,128)):
        self._screen.blit(self._font.render(text,1,color),position)

    def update(self):
        for v in self._vehicules:
            v.steerUpdate(self._track, self._vehicules)
        Vehicule.updatePositions(self._vehicules)
        Vehicule.handleCollisions(self._vehicules)
        self.drawMe()

    def eventClic(self,coord,b):
        ### ADDED to generate random speed and force
        vehiculeSpeed = (random.randrange(2,20),random.randrange(2,20))
        vehiculeForce = (random.randrange(0,10),random.randrange(0,10))
        print("Adding Vehicule at ({},{}) of radius {} radius with a speed of {} and has a {} force".format(coord[0],coord[1], self._vehiculeRadius, vehiculeSpeed, vehiculeForce))
        self._vehicules.append(Vehicule((coord[0],coord[1]), radius=self._vehiculeRadius, speed=vehiculeSpeed, force=vehiculeForce))
    def recordMouseMove(self, coord):
        self._mouseCoords = coord
    ### ADDED
    def recordVehiculeSize(self, update):
        if self._vehiculeRadius + update >= Vehicule._minradius and self._vehiculeRadius + update <= Vehicule._maxradius:
            self._vehiculeRadius += update
        
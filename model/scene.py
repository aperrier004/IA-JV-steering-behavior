import pygame

# ----------------------------------------
import utils
from model.track     import Track
from model.vehicule  import Vehicule
# ----------------------------------------

class Scene:
    _track= None
    _vehicules = None
    _screen = None
    _font = None
    ### ADDED
    _vehiculeSize = 6

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
        
        ### ADDED
        # draw vehicule size
        textToShow = "Vehicule's size: {}".format(self._vehiculeSize).encode()
        textSurface = self._font.render(textToShow, False, (255,255,255))
        self._screen.blit(textSurface, (10, utils.__screenSize__[1] -30))

        textToShow = "Use mouse's wheel to control vehicule's size".encode()
        textSurface = self._font.render(textToShow, False, (255,255,255))
        self._screen.blit(textSurface, (10, utils.__screenSize__[1] -15))
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
        print("Adding Vehicule at ({},{}) of size {} radius".format(coord[0],coord[1], self._vehiculeSize))
        self._vehicules.append(Vehicule((coord[0],coord[1]), radius=self._vehiculeSize))
    def recordMouseMove(self, coord):
        self._mouseCoords = coord
    ### ADDED
    def recordVehiculeSize(self, update):
        if self._vehiculeSize + update >= Vehicule._minradius and self._vehiculeSize + update <= Vehicule._maxradius:
            self._vehiculeSize += update
        
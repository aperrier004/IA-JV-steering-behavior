# Objectifs :
# faire bouger le chemin en temps réel + circuit plus gros
# Faire des véhicules de taille, force et vitesse différentes #OK
# Résolution de conflits : ajouter des dommages aux véhicules qui se touchent

import sys, math
import pygame
import pygame.draw

# ----------------------------------
from model.scene    import Scene
# ----------------------------------

MOUSE_LEFT         = 1
MOUSE_MIDDLE       = 2
MOUSE_RIGHT        = 3
MOUSE_WHEEL_UP     = 4
MOUSE_WHEEL_DOWN   = 5

def main():
    scene = Scene()
    done = False
    clock = pygame.time.Clock()
    while done == False:
        clock.tick(20)
        scene.update()
        scene.drawMe()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: done=True
            if event.type == pygame.KEYDOWN: done=True
            if event.type == pygame.MOUSEWHEEL:
                scene.recordVehiculeSize(event.y)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == MOUSE_LEFT:
                    scene.eventClic(event.dict['pos'],event.dict['button'])
            elif event.type == pygame.MOUSEMOTION:
                scene.recordMouseMove(event.dict['pos'])

    pygame.quit()

if not sys.flags.interactive: main()


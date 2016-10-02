import pygame
from pygame.locals import *

from constantes import *

def credits(screen, lang, levelNumber):

    continuer = True
    position = pygame.Rect(0, 0, 0, 0)
    tempsActuel = 0
    tempsPrecedent = 0


    # Charge image credit
    creditsImg = pygame.image.load(SOURCE_IMG + 'credit.jpg').convert()

    # position de départ
    position.x = 0
    position.y = 0

    # blit et affiche écran
    screen.fill(BLACK)                  # Ecran tout noir
    screen.blit(creditsImg, position)
    pygame.display.flip()               # mise a jour ecran
    pygame.time.delay(3000)             # délai

    while continuer:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            if event.dict['unicode'] == 'q' or event.key == K_ESCAPE:   # sortie
               continuer = 0

        tempsActuel = pygame.time.get_ticks()
        if tempsActuel - tempsPrecedent >= 100:       # toutes les 100 ms
            position.y += 5                           # le texte descend
            tempsPrecedent = tempsActuel
            if position.y > creditsImg.get_height() + 100:  # de pixels
                continuer = 0

        screen.fill(BLACK)                  # Ecran tout noir
        screen.blit(creditsImg, position)
        pygame.display.flip()               # mise a jour ecran

    levelNumber = 1     #reprend au niveau 1


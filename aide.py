import pygame
from pygame.locals import * # pour les constantes touches...
from constantes import *
from general import *


def aide(screen, mode, lang, langu):
    nombreDeLignes = 0
    continuer = True
    position = pygame.Rect(0, 0, 0, 0)


    # load background img
    reka = pygame.image.load(SOURCE_IMG + 'options.jpg').convert()

    # init lang
    sourceFile = SOURCE_FILE + 'lang.lvl'
    lignes = compteLignes(sourceFile)
    initialiseHelpTable(sourceFile, lignes, langu)

    # choix de la langue
    pathFile = langu[lang].data

    # dans laquelle on affiche les textes pour jeu ou édition en fonction du mode
    if mode == GAME:
        sourceFile = SOURCE_FILE + pathFile + '/helpJeu.lvl'
    else:
        sourceFile = SOURCE_FILE + pathFile + '/helpEdit.lvl'

    nombreDeLignes = compteLignes(sourceFile)

    # now we can create the variable for the structure
    tableau = [Text() for i in range(nombreDeLignes)]
    initialiseHelpTable(sourceFile, nombreDeLignes, tableau)

    # whiteBar
    whiteBar = pygame.Surface((screen.get_width(), 30), screen.get_flags())
    whiteBar.fill(WHITE)

    while continuer:
        event = pygame.event.wait()
        if event.type == QUIT:
            continuer = False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                continuer = False
            if event.key == K_r:
                continuer = False

        # blit and show screen
        position.x = 0
        position.y = 0
        screen.fill(BLACK)
        screen.blit(reka, position)

        # write the text
        # title
        police = pygame.font.Font('angelina.ttf', 50)
        tableau[0].partie = police.render(tableau[0].data, True, WHITE)
        position.x = (screen.get_width() - tableau[0].partie.get_width())//2
        position.y = 50
        screen.blit(tableau[0].partie, position)

        # subtitle
        police = pygame.font.Font('angelina.ttf', 25)
        position.y += 50
        tableau[1].partie = police.render(tableau[1].data, True, WHITE)
        screen.blit(tableau[1].partie, position)

        position.x = 30
        position.y = 140
        police = pygame.font.Font('angelina.ttf', 20)
        for i in range(3, nombreDeLignes):
            if position.y < screen.get_height() - whiteBar.get_height():
                tableau[i].partie = police.render(tableau[i].data, True, WHITE)
                screen.blit(tableau[i].partie, position)
            else:
                position.x = 230
                position.y = 140
                if position.y < screen.get_height() - whiteBar.get_height():
                    tableau[i].partie = police.render(tableau[i].data, True, WHITE)
                    screen.blit(tableau[i].partie, position)
            position.y += 30

        # blit white bar
        position.x = 0
        position.y = screen.get_height() - whiteBar.get_height()
        screen.blit(whiteBar, position)

        # blit exit
        retour = police.render(tableau[2].data, True, BLUE)
        position.x = 10
        position.y = (screen.get_height() - whiteBar.get_height()) + 5
        screen.blit(retour, position)

        pygame.display.update()
    pygame.event.clear()

import pygame, sys, os
from pygame.locals import * # pour les constantes touches...

from constantes import *
from general import *
from jeu import *
from options import *
from edit import *

def main():

    lang = FR

    mouseover = False
    difficulty = False           # True
    soundly = False            # True

    levelNumber = 1
    levelFinal = 0

    fondBlanc = 1       # indique la texte qui est en surbrillance, du haut -> bas 1 2 3

    # init
    pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
    pygame.init()                                            # initialize pygame
    pygame.font.init()


    # set video
    pygame.display.set_caption('Mon Mario Sokoban!') # titre de la fenetre

    screen = pygame.display.set_mode((408, 468), pygame.HWSURFACE or pygame.SDL_DOUBLEBUF, 32)

    # menu
    menu = pygame.image.load(SOURCE_IMG + 'menu.jpg').convert() # charge image menu de depart
    menuPos = pygame.Rect(0,  0, 408, 408)

    # levelFinal
    levelFinal = len(os.listdir(SOURCE_LEVELS))

    # langues
    sourceFile = SOURCE_FILE + "lang.lvl"
    lignes = compteLignes(sourceFile)

    langu = []      # contient nbr de langues * class Text()
    for i in range(0, lignes):
        langu.append(Text())

    initialiseHelpTable(sourceFile,lignes,langu)    # Text.data de langu recoit en et fr

    # define language
    pathFile = langu[lang].data

    # define sourceFile
    sourceFile = SOURCE_FILE + pathFile + '/main.lvl'

    # compte lignes
    lignes = compteLignes(sourceFile)

    # init table
    tableau = [Text() for i in range(lignes)]
    initialiseMainTable(sourceFile,lignes,tableau)      # place les textes dans Text() -> data
    # 1 : Jouez 2 : Editez Niveaux 3 : Options  Produit par AstroProduction  Q : Quitter      ou
    # 1 : Play 2 : Edit Level 3 : Options Build By AstroProduction Q : Exit
    shadeMainText(lignes,tableau,0)                # place les images des textes dans Text() -> partie

    # position text
    tableau[0].positionY = 180          # place les coord positionX et Y des Text()
    for i in range(0, 3):
        # tableau[i].positionX = (screen.get_width() - tableau[i].partie.get_width())//2
        tableau[i].positionX = 140
        if i > 0:
            tableau[i].positionY = tableau[i].positionY + (tableau[i-1].positionY + 50)
    tableau[3].positionX = (screen.get_width() - tableau[3].partie.get_width())-20
    tableau[3].positionY = (screen.get_height() - tableau[3].partie.get_height())-10
    tableau[4].positionX = 10
    tableau[4].positionY=(screen.get_height() - tableau[4].partie.get_height())-10

    # event
    continuer = 1
    while continuer:

        for e in pygame.event.get():

            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_q): # sortie par bouton x ou Echap
                continuer = 0

            elif e.type == MOUSEBUTTONDOWN:
                if e.button == LEFT:       # bouton gauche
                    if mouseover:
                        if fondBlanc == 1:
                            mode = GAME
                            jouer(screen, levelNumber, lang, langu,levelFinal, difficulty, soundly, mode)
                            if levelNumber > levelFinal:
                                credits(screen, lang, levelNumber)
                                continue

                        elif fondBlanc == 2:
                            mode = EDIT
                            edit(screen, levelNumber, mode, lang, langu, levelFinal)
                            continue

                        elif fondBlanc == 3:
                            lang, difficulty, soundly = options(screen, lang, langu, difficulty, soundly)
                            pathFile = printLang(lang)       #, pathFile)
                            sourceFile = SOURCE_FILE + pathFile + '/main.lvl'
                            initialiseMainTable(sourceFile, lignes, tableau)
                            shadeMainText(lignes, tableau, 2)

            elif e.type == MOUSEMOTION:
                motionX,  motionY = e.pos
                if (motionX > tableau[0].positionX and \
                motionX < (tableau[0].positionX+ tableau[0].partie.get_width())) and \
                (motionY > tableau[0].positionY and \
                motionY < (tableau[0].positionY+ tableau[0].partie.get_height())):
                    shadeMainText(lignes,tableau,0)
                    fondBlanc = 1
                    mouseover = True

                elif (motionX > tableau[1].positionX and \
                motionX < (tableau[1].positionX+ tableau[1].partie.get_width())) and \
                (motionY > tableau[1].positionY and \
                motionY < (tableau[1].positionY+ tableau[1].partie.get_height())):
                    shadeMainText(lignes,tableau,1)
                    fondBlanc = 2
                    mouseover = True

                elif (motionX > tableau[2].positionX and \
                motionX < (tableau[2].positionX+ tableau[2].partie.get_width())) and \
                (motionY > tableau[2].positionY and \
                motionY < (tableau[2].positionY+ tableau[2].partie.get_height())):
                    shadeMainText(lignes,tableau,2)
                    fondBlanc=3
                    mouseover=1
                else:
                    mouseover= False

        screen.fill(BLACK)              # Ecran tout noir -> efface tout l'écran
        screen.blit(menu, menuPos)      # Affiche le fond du menu (menu.jpg)
        # puis affichage de tous les textes: Jouez Editez Niveaux Options Produit par AstroProduction Q : Quitter
        # fichier ./files/fr/main.lvl   idem pour /en
        for i in range(lignes):
            screen.blit(tableau[i].partie, (tableau[i].positionX, tableau[i].positionY))
        # affiche tout à l'écran
        pygame.display.flip() # mise a jour ecran

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()

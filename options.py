import pygame
from pygame.locals import * # pour les constantes touches...
from constantes import *
from general import *
from globales import *

def options(screen, lang, langu, difficulty, soundly):

    # global soundly          #difficulty,

    loop = True
    position = pygame.Rect(0, 0, 0, 0)
    fondBlanc = 1

    mouseover = False

    if difficulty:
        modulo7 = False
    else:
        modulo7 = True

    if soundly:
        modulo5 = True
    else:
        modulo5 = False

    # initialise image de fond
    fond = pygame.image.load(SOURCE_IMG + "options.jpg")
    position.x = 0
    position.y = 0

    # initialise police et texte
    pygame.font.init()
    police = pygame.font.Font('angelina.ttf', 20)

    # define language
    pathFile = langu[lang].data     # 'fr' ou 'en'

    # define sourceFile default
    sourceFile = SOURCE_FILE + pathFile + '/options.lvl'    # ./files/fr ou en/options.lvl
    lignes = compteLignes(sourceFile)
    tableau = [Text() for i in range(lignes)]

    # initialise en fr ou en
    initialiseTable(sourceFile, lignes, tableau)
    # Options Retour: Esc 1: Langues FRANCAIS 2: Son ALLUMER 3: Difficulte AUCUNE ETEINT CONTRE LE TEMPS
    # Options Back: Esc 1: Languages ENGLISH 2: Sound ON 3: Difficulty NONE OFF CHRONO WAR

    # initialise surbrillance et titre au départ
    tableau[3].partie = police.render(tableau[3].data, True, GREEN, BLACK) # Langes ou Languages en surbrillance
    police = pygame.font.Font('angelina.ttf', 70)
    tableau[0].partie = police.render(tableau[0].data, True, WHITE) # Options en blanc taille 70 pour le titre

    # init loop
    while loop:
        event = pygame.event.wait()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): # sortie par bouton x ou Echap:
            loop = False

        if event.type == MOUSEMOTION:
            motionX, motionY = event.pos
            police = pygame.font.Font('angelina.ttf', 20)
            if motionX > 210 and motionX < 210 + tableau[3].partie.get_width() \
            and motionY > 210 and motionY < 210 + tableau[3].partie.get_height():
                mouseover = True
                fondBlanc = 1   # --> surbrillance Langue
                shadeText(lignes, tableau, 3)
            elif motionX > 210 and motionX < 210 + tableau[5].partie.get_width()\
            and motionY > 270 and motionY < 270 + tableau[5].partie.get_height():
                mouseover = True
                fondBlanc = 2   # --> surbrillance Son
                if modulo5:
                    shadeText(lignes, tableau, 5)   # Allumé
                else:
                    shadeText(lignes, tableau, 8)   # Eteint
            elif motionX > 210 and motionX < 210 + tableau[7].partie.get_width()\
            and (motionY > 330 and motionY < 330 + tableau[7].partie.get_height()):
                mouseover = True
                fondBlanc = 3      # --> surbrillance Difficulté
                if modulo7:
                    shadeText(lignes, tableau, 7)   # Aucune
                else:
                    shadeText(lignes, tableau, 9)   # Contre le chrono
            else:
                mouseover = False

        if event.type == MOUSEBUTTONDOWN:
            if event.button == LEFT:
                if mouseover:
                    if fondBlanc == 2:
                        if modulo5:             # son
                            modulo5 = False
                            shadeText(lignes, tableau, 8)
                            soundly = False
                        else:
                            modulo5 = True
                            shadeText(lignes, tableau, 5)
                            soundly = True
                    elif fondBlanc == 3:        # difficulté
                        if modulo7:
                            modulo7 = False
                            shadeText(lignes, tableau, 9)   # Contre le temps
                            difficulty = True
                        else:
                            modulo7 = True
                            shadeText(lignes, tableau, 7)   # Aucune
                            difficulty = False
                    else:
                        sourceFile = SOURCE_FILE + 'lang.lvl'
                        lignes = compteLignes(sourceFile)
                        if lang == lignes - 1:
                            lang = EN
                        else:
                            lang += 1   # --> FR
                        pathFile = langu[lang].data
                        sourceFile = SOURCE_FILE + pathFile + '/options.lvl'
                        lignes = compteLignes(sourceFile)
                        initialiseTable(sourceFile, lignes, tableau)

                        police = pygame.font.Font('angelina.ttf', 70)
                        tableau[0].partie = police.render(tableau[0].data, True, WHITE)
                        shadeText(lignes, tableau, 3)
            #     continue
            # continue

        screen.fill(BLACK)          # Ecran tout noir

        # blit fond
        position.x = 0
        position.y = 0
        screen.blit(fond, position)

        # blit Options
        position.x = (screen.get_width() - tableau[0].partie.get_width())//2
        position.y = 40
        screen.blit(tableau[0].partie, position)

        # blit les sous-menus
        position.y = 180
        for i in range(2,(lignes-2)):
            if i % 2 == 0:
                position.x = 150
                screen.blit(tableau[i].partie, position)
            else:
                # position.x = (screen.get_width() - tableau[i].partie.get_width())//2
                position.x = 210
                if(i == 5 and modulo5 == False):
                    screen.blit(tableau[i+3].partie, position)

                    # soundly[0] = 0
                elif i == 7 and modulo7 == False:
                    screen.blit(tableau[i+2].partie, position)
                    difficulty = True
                else:
                    screen.blit(tableau[i].partie, position)
            position.y += 30

        # place the back button:
        position.x = 10
        position.y = (screen.get_height() - tableau[1].partie.get_height())-10
        screen.blit(tableau[1].partie, position)
        pygame.display.flip() # mise a jour ecran
        pygame.event.clear()

        allOptions = [lang, difficulty, soundly]
    return allOptions

import pygame
from pygame.locals import *  # pour les constantes touches...
from constantes import *
from fichiers import *
from general import *
from aide import *

def edit(screen, levelNumber ,mode, lang, langu, levelFinal):

    continuer = True
    motionX = 0
    motionY = 0
    alsoMario = 0
    carte = [[int for lgn in range(NB_BLOCS_HAUTEUR)]for col in range(NB_BLOCS_LARGEUR)]
    restMario = 0
    levelWord = ''
    clicGaucheEnCours = False
    clicDroitEnCours = False
    saved = False
    objectPos = pygame.Rect(0,0,0,0)
    exemplePos = pygame.Rect(0,0,0,0)

    # charger images
    mur = pygame.image.load(SOURCE_IMG + 'mur.jpg').convert()
    mur50 = pygame.image.load(SOURCE_IMG + 'mur50.jpg').convert()
    caisse = pygame.image.load(SOURCE_IMG + 'caisse.jpg').convert()
    caisse50 = pygame.image.load(SOURCE_IMG + 'caisse50.jpg').convert()
    caisse_ok = pygame.image.load(SOURCE_IMG + 'caisse_ok.jpg').convert()
    caisse_ok50 = pygame.image.load(SOURCE_IMG + 'caisse_ok50.jpg').convert()
    objectif = pygame.image.load(SOURCE_IMG + 'objectif.png').convert_alpha()
    objectif50 = pygame.image.load(SOURCE_IMG + 'objectif50.png').convert_alpha()
    mario = pygame.image.load(SOURCE_IMG + 'mario_bas.gif').convert_alpha()
    mario50 = pygame.image.load(SOURCE_IMG + 'mario_bas50.gif').convert_alpha()
    quadrillage = pygame.image.load(SOURCE_IMG + 'quadrillage.png').convert_alpha()

    # objet par défaut
    objet = MUR

    # load map
    chargeCarte(carte, levelNumber)

    # search mario
    for i in range(NB_BLOCS_LARGEUR):
        for j in range(NB_BLOCS_HAUTEUR):
            if carte[i][j] ==MARIO:
                alsoMario += 1

    # white Bar
    whiteBar = pygame.Surface((screen.get_width(), 60), screen.get_flags())
    whiteBar.fill(WHITE)

    # police
    police = pygame.font.Font('angelina.ttf', 20)

    # define sourceFile default
    pathFile = printLang(lang)                          # 'fr' ou 'en'
    sourceFile = SOURCE_FILE + pathFile + '/edit.lvl'    # './files/'fr' ou 'en'/edit.lvl'
    # H: Help  Level:  Saved  ESC: Exit ou H: Aide  Niveau:  Sauve  ESC: Quitter

    # nombre de lignes
    lignes = compteLignes(sourceFile)
    tableau = [Text() for i in range(lignes)]

    # initialise tableau en fr ou en
    initialiseEditTable(sourceFile,lignes,tableau)
    levelWord = tableau[1].data
    tableau[1].data = levelWord + ' ' + str(levelNumber)
    tableau[1].partie = police.render(tableau[1].data, True, BLUE)

    # event
    while(continuer):

        # check if there is mario on the map if not initialize the boolean
        if(objet == MARIO and alsoMario != 0):
            for i in range(NB_BLOCS_LARGEUR):
                for j in range(NB_BLOCS_LARGEUR):
                    if carte[i][j]==MARIO:
                        restMario += 1
            if restMario == 0:
                alsoMario = 0
            restMario=0

        for event in pygame.event.get():

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                continuer = False      # sortie de la boucle

            if event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    continuer = False

                elif event.key == K_1 or event.key == K_KP1:
                    objet = MUR

                elif event.key == K_2 or event.key == K_KP2:
                    objet = CAISSE

                elif event.key == K_3 or event.key == K_KP3:
                    objet = OBJECTIF

                elif event.key == K_4 or event.key == K_KP4:
                    objet = MARIO

                elif event.key == K_5 or event.key == K_KP5:
                    objet = CAISSE_OK

                elif event.key == K_h and lang == EN:
                    aide(screen,mode,lang,langu)


                elif event.key == K_a and lang == FR:
                    aide(screen,mode,lang,langu)

                elif event.key == K_s:
                    saved = True
                    sauveCarte(carte,levelNumber)

                elif event.key == K_PAGEUP:
                    if levelNumber <= levelFinal:
                        levelNumber += 1
                        if levelNumber == levelFinal+ 1:
                            carte = [[MUR for lgn in range(NB_BLOCS_HAUTEUR)]for col in range(NB_BLOCS_LARGEUR)]
                            tableau[1].data = levelWord + ' ' + str(levelNumber)
                            tableau[1].partie = police.render(tableau[1].data, True, BLUE)
                            break
                        else:
                            # add level number to tableau[1]
                            tableau[1].data = levelWord + ' ' + str(levelNumber)
                            tableau[1].partie = police.render(tableau[1].data, True, BLUE)
                            chargeCarte(carte, levelNumber)

                elif event.key == K_PAGEDOWN:
                    if levelNumber > 1:
                        levelNumber -=1
                        # add level number to tableau[1]
                        tableau[1].data = levelWord + ' ' + str(levelNumber)
                        tableau[1].partie = police.render(tableau[1].data, True, BLUE)
                        chargeCarte(carte, levelNumber)

            if event.type == MOUSEBUTTONDOWN:
                motionY,  motionX = event.pos
                if motionX <= 408 and motionY <= 408:
                    if event.button == RIGHT:
                        clicDroitEnCours = True
                        carte[motionX // TAILLE_BLOC][motionY // TAILLE_BLOC] = VIDE
                    if event.button == LEFT:
                        clicGaucheEnCours = True
                        if objet == MARIO and alsoMario != 0:       # mario can be put only once.
                            continue
                        else:
                            carte[motionX // TAILLE_BLOC][motionY // TAILLE_BLOC] = objet
                            if objet == MARIO:
                                alsoMario +=1

            if event.type == MOUSEBUTTONUP:
                if event.button == LEFT:
                    clicGaucheEnCours = False
                elif event.button == RIGHT:
                    clicDroitEnCours = False

            if event.type == MOUSEMOTION:
                motionX,  motionY = event.pos
                exemplePos.x = motionX + 20
                exemplePos.y = motionY + 20

        # screen
        screen.fill(BLACK)      # Ecran tout noir

        # affichage carte
        for lgn in range (NB_BLOCS_HAUTEUR):
            for col in range (NB_BLOCS_LARGEUR):
                objectPos.x = col * TAILLE_BLOC
                objectPos.y = lgn * TAILLE_BLOC
                if carte[lgn][col] == MUR:
                    screen.blit(mur, objectPos)
                elif carte[lgn][col] == CAISSE:
                    screen.blit(caisse,objectPos)
                elif carte[lgn][col] == CAISSE_OK:
                    screen.blit(caisse_ok,objectPos)
                elif carte[lgn][col] == OBJECTIF:
                    screen.blit(objectif,objectPos)
                elif carte[lgn][col] == MARIO:
                    screen.blit(mario, objectPos)
        screen.blit(quadrillage, (0, 0))

        # whiteBar
        objectPos.x = 0
        objectPos.y = screen.get_height() - whiteBar.get_height()
        screen.blit(whiteBar,objectPos)

        # text
        objectPos.x = 10
        objectPos.y = (screen.get_height() - whiteBar.get_height()) + 5
        screen.blit(tableau[0].partie,objectPos)
        objectPos.x = 100
        screen.blit(tableau[1].partie,objectPos)

        if saved:
            objectPos.x = 200
            screen.blit(tableau[2].partie,objectPos)
        objectPos.x = (screen.get_width() - tableau[3].partie.get_width()) - 10
        screen.blit(tableau[3].partie,objectPos)

        # blit exemple
        if objet == MUR:
            screen.blit(mur50, exemplePos)
        elif objet == CAISSE:
            screen.blit(caisse50, exemplePos)
        elif objet == CAISSE_OK:
            screen.blit(caisse_ok50, exemplePos)
        elif objet == OBJECTIF:
            screen.blit(objectif50, exemplePos)
        elif objet == MARIO:
            screen.blit(mario50, exemplePos)

        # mise a jour affichage de l'écran ---------------------
        pygame.display.flip()

        if saved:
            pygame.time.delay(2000)
            objectPos.x = 10
            objectPos.y = (screen.get_height() - whiteBar.get_height()) + 5
            screen.blit(tableau[0].partie, objectPos)
            objectPos.x = 100
            screen.blit(tableau[1].partie, objectPos)
            objectPos.x = (screen.get_width() - tableau[3].partie.get_width())-10
            screen.blit(tableau[3].partie, objectPos)
            saved = False


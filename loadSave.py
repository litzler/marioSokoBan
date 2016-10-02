import pygame, sys
from pygame.locals import * # pour les constantes touches...

from constantes import *
from fichiers import *
from jeu import *
from  general import *

def loadSaveMenu (screen, levelNumber, saveNumber, carte, joueurPos, levelFinal):

    continuer=1
    fondBlanc=1
    i=0
    y=0
    longueurLigne=0
    mouseOver=0
    caractere = []
    clevel = []
    cpercent = []
    # SDL_Surface *reka=NULL;
    position = pygame.Rect(0, 0, 0, 0)
    # SDL_Event event;
    # SDL_Color noir={0,0,0};
    # SDL_Color blanc={255,255,255};
    # TTF_Font *police=NULL;

    # initialise police
    pygame.font.init()
    police = pygame.font.Font('angelina.ttf', 20)

    # load LoadSave Img
    reka = pygame.image.load(SOURCE_IMG + "loadSave.jpg")

    # percent=(100*levelNumber)/LEVEL_FINAL

    # init pos
    position.x=0
    position.y=0

    screen.fill(BLACK)
    screen.blit(reka, position)
    position.x=50;
    position.y=180;

    lignes = compteLignes(SOURCE_FILE + "load.lvl")

    # f = [['' for i in range(lignes)] for j in range(NOMBRE_DE_SAVE)]
    tableau = [Text() for i in range(lignes)]

    # Chargement du fichier --> structures Text() du tableau
    f = open(SOURCE_FILE + 'load.lvl','r')
    for i in range(NOMBRE_DE_SAVE):
        fichier = f.readline().split()
        for j in range(NOMBRE_DE_SAVE):
            tableau[i].id = fichier[0]
            tableau[i].data = fichier[1]
            tableau[i].level = fichier[2]
            tableau[i].percent = fichier[3]

    # Ecriture des lignes
    police = pygame.font.Font('angelina.ttf', 25)
    for i in range(NOMBRE_DE_SAVE):
        tableau[i].pourcent = str(tableau[i].id)+' :   '+str(tableau[i].data)+'  Level:  '+str(tableau[i].level)+'   '+str(tableau[i].percent)     # +  +  +

        if(tableau[i].id == fondBlanc):
            tableau[i].partie = police.render(tableau[i].pourcent, True, BLACK, WHITE)
        else:
            tableau[i].partie = police.render(tableau[i].pourcent, True, WHITE)

        if(i > 0):
            position.y += 60
        screen.blit(tableau[i].partie, position)

        if saveNumber == 2:
            continuer=0
            levelNumber = getData(saveNumber,tableau,fondBlanc,carte,joueurPos,levelNumber,levelFinal)
        else:
            # mise a jour de l'ecran
            pygame.display.flip()

    while (continuer):

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                continuer = 0      # sortie de la boucle

            elif event.type == KEYDOWN:
                police = pygame.font.Font('angelina.ttf', 25)
                if event.key == K_ESCAPE or event.key == K_q:
                    continuer=0
                if event.key == K_1 or event.key == K_KP1:
                    fondBlanc=1
                if event.key == K_2 or event.key == K_KP1:
                    fondBlanc=2
                if event.key == K_3 or event.key == K_KP3:
                    fondBlanc=3
                if event.key == K_4 or event.key == K_KP4:
                    fondBlanc=4
                if event.key == K_DOWN:
                    if fondBlanc < NOMBRE_DE_SAVE:
                        fondBlanc += 1
                if event.key == K_UP:
                    if fondBlanc > NOMBRE_DE_SAVE:
                        fondBlanc -= 1
                if event.key == K_RETURN:
                    # load
                    getData(saveNumber,tableau,fondBlanc,carte,joueurPos,levelNumber,levelFinal)
                    continuer=0

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == LEFT:
                    if mouseOver:
                        levelNumber = getData(saveNumber,tableau,fondBlanc,carte,joueurPos,levelNumber,levelFinal)
                        continuer=0

            elif event.type == MOUSEMOTION:
                mouseOver=0
                position.y=180
                for i in range(NOMBRE_DE_SAVE):
                    motionX,  motionY = event.pos
                    if (motionX > position.x and motionX < position.x + tableau[i].partie.get_width())\
                    and (motionY > position.y and motionY < position.y + tableau[i].partie.get_height()):
                        fondBlanc = tableau[i].id
                        mouseOver = 1
                    # else:
                    #     mouseOver=0
                    position.y += 60

        position.y = 180
        for i in range(NOMBRE_DE_SAVE):
            if(tableau[i].id == fondBlanc):
                tableau[i].partie = police.render(tableau[i].pourcent, True, BLACK, WHITE)
            else:
                tableau[i].partie = police.render(tableau[i].pourcent, True, WHITE, BLACK)
            if(i > 0):
                position.y += 60
            screen.blit(tableau[i].partie, position)
        pygame.display.flip()

    # mise a jour de l'ecran
    pygame.display.flip()
    return (int(levelNumber))

def getData(saveNumber, tableau, fondBlanc, carte, joueurPos, levelNumber, levelFinal):
    if saveNumber == 2:
        saveNumber = 1

    if saveNumber == 0:
        for i in range(NOMBRE_DE_SAVE):
            if tableau[i].id == fondBlanc:
                chargeCarte(carte,tableau[i].level)
                searchMario(carte,joueurPos)
                levelNumber = tableau[i].level
    # save
    else:
        f = open(SOURCE_FILE + 'load.lvl','w')

        for i in range(NOMBRE_DE_SAVE):
            if tableau[i].id == fondBlanc:
                tableau[i].level = levelNumber
                tableau[i].percent = (100*levelNumber)/levelFinal
            f.write('%s %s %s %s\n' % (tableau[i].id, tableau[i].data, tableau[i].level, tableau[i].percent))
        f.close()
    saveNumber=0
    return (int(levelNumber))

def searchMario(carte, joueurPos):     #, joueurDebut, joueurPos):     # Recherche de Mario
    for lgn in range(NB_BLOCS_HAUTEUR):             # et mise à jour de
        for col in range(NB_BLOCS_LARGEUR):         # ses coordonnées
            if carte[lgn][col] == MARIO:
                # joueurDebut.x = lgn
                # joueurDebut.y = col
                joueurPos.x = col
                joueurPos.y = lgn
                carte[lgn][col] = VIDE              # vide sa case
    return

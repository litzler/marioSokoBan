import pygame
from constantes import *

class Text:
    id = 0
    level = 0
    percent= 0.00000
    data = []                   # le texte
    positionX = 0               # coord x
    positionY = 0               # coord y
    partie = pygame.Surface     # la surface à afficher

def compteLignes(nomDuFichier):         # compte le nombre de lignes du niveau
    fichier = open(nomDuFichier, "r")
    f = fichier.read()
    fichier.close()
    lignes = 0
    for c  in range(len(f)):
        if f[c] == '\n':
            lignes += 1
    return lignes

def levFinal(nomDuFichier):
    fichier = open(nomDuFichier,"r")
    f = fichier.read()
    fichier.close()
    n = int(f)
    return n

def initialiseHelpTable(sourceFile,lignes,langu):
    fichier = open(sourceFile,"r")
    for i in range(0, lignes):
        langu[i].data = fichier.readline()
        langu[i].data = langu[i].data[0 : -1]   # enleve le '\n' final
    fichier.close()

def initialiseMainTable(sourceFile,lignes,tableau):
    fichier = open(sourceFile,"r")
    for i in range(0,  lignes):
        if i<3:
            police = pygame.font.Font('angelina.ttf', 30)
        else:
            police = pygame.font.Font('angelina.ttf', 20)
        tableau[i].data = fichier.readline()
        tableau[i].data = tableau[i].data[0 : -1]
        tableau[i].partie = police.render(tableau[i].data, True, WHITE, BLACK)

def shadeMainText(lignes, tableau, k):
    police = pygame.font.Font('angelina.ttf', 30)
    for i in range(0, 3):
        if i < 3:
            police = pygame.font.Font('angelina.ttf', 30)
        else:
            police = pygame.font.Font('angelina.ttf', 20)
        if i != k:
            tableau[i].partie = police.render(tableau[i].data, True, GREEN, BLACK)     #WHITE, BLACK)
        else:
            tableau[i].partie = police.render(tableau[i].data, True, WHITE, BLACK)

def printLang(lang): 
    if lang == FR:
        pathFile = 'fr'
    else:
        pathFile = 'en'
    return pathFile

def initialiseGameTable(file, lignes, tableau):
    fichier = open(file,"r")
    for i in range(lignes):
        if i<3:
            police = pygame.font.Font('angelina.ttf', 80)
        else:
            police = pygame.font.Font('angelina.ttf', 20)
        tableau[i].data = fichier.readline()
        tableau[i].data = tableau[i].data[0 : -1]
        tableau[i].partie = police.render(tableau[i].data, True, BLUE)
    fichier.close()

def initialiseTable(file, lignes, tableau):
    fichier = open(file,"r")
    for i in range(lignes):
        if i % 2 == 0 and i != 8:
            police = pygame.font.Font('angelina.ttf', 30)
        else:
            police = pygame.font.Font('angelina.ttf', 20)
        tableau[i].data = fichier.readline()
        tableau[i].data = tableau[i].data[0 : -1]
        tableau[i].partie = police.render(tableau[i].data, True, WHITE)
    fichier.close()

def shadeText(lignes, tableau, k):
    police = pygame.font.Font('angelina.ttf', 30)
    for i in range(1, lignes):
        if i % 2 == 0 and i != 8:
            police = pygame.font.Font('angelina.ttf', 30)
        else:
            police = pygame.font.Font('angelina.ttf', 20)
        if i != k:
            tableau[i].partie = police.render(tableau[i].data, True, WHITE)
        else:   # //fondblanc pour Francais/English
            tableau[i].partie = police.render(tableau[i].data, True, GREEN, BLACK)

def initialiseEditTable(file, lignes, tableau):
    police = pygame.font.Font('angelina.ttf', 20)
    fichier = open(file,"r")
    for i in range(lignes):
        tableau[i].data = fichier.readline()
        tableau[i].data = tableau[i].data[0 : -1]
        tableau[i].partie = police.render(tableau[i].data, True, BLUE)
    fichier.close()

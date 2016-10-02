import pygame

SOURCE_IMG = "./files/images/"
SOURCE_FILE = "./files/"
SOURCE_LEVELS = "./files/levels/"

EN = 0
FR = 1

TAILLE_BLOC = 34    # Taille d'un bloc (carre) en pixels

NB_BLOCS_LARGEUR = 12
NB_BLOCS_HAUTEUR = 12
NB_CASES =12

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (41, 90, 245)
GRAY = (41, 90, 245)
GREEN = (0, 255, 0)

GAME = 0
EDIT = 1
OPTION = 2

# perso
mario = [ pygame.Surface for i in range(4)]

HAUT = 0
BAS = 1
GAUCHE = 2
DROITE = 3

VIDE = 0
MUR = 1
CAISSE = 2
OBJECTIF = 3
MARIO = 4
CAISSE_OK = 5
MARIO_OBJ = 6

LEFT = 1
RIGHT = 3

NOMBRE_DE_SAVE = 4

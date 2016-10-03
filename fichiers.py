from constantes import *

def chargeCarte(carte, levelNumber):
    tableau = [' ']
    for lgn in range(NB_BLOCS_LARGEUR):  # RAZ
        for col in range(NB_BLOCS_HAUTEUR):
            carte[lgn][col] = 0
    fichier = open(SOURCE_LEVELS + 'level' + str(levelNumber) + '.lev', "r")
    f = fichier.read()
    fichier.close()
    while len(tableau) > 0: tableau.pop()
    tableau.append(' ')
    for i in range(0, len(f)):  # tranfert des donnees fichier --> tableau
        if f[i] != '\n':
            tableau.append(f[i])
    n = 1
    for lgn in range(0, NB_BLOCS_HAUTEUR):
        for col in range(0, NB_BLOCS_LARGEUR):
            if tableau[n] == ' ':
                carte[lgn][col] = VIDE
            if tableau[n] == '#':
                carte[lgn][col] = MUR
            if tableau[n] == '.':
                carte[lgn][col] = OBJECTIF
            if tableau[n] == '$':
                carte[lgn][col] = CAISSE
            if tableau[n] == '*':
                carte[lgn][col] = CAISSE_OK
            if tableau[n] == '@':
                carte[lgn][col] = MARIO
            # if tableau[n] == '+':
            #     carte[l
            # ][lgn] = MARIO_OBJ
            n += 1
    return


def sauveCarte(carte, levelNumber):
    f = open(SOURCE_LEVELS + 'level' + str(levelNumber) + '.lev', "w")
    ligne = []
    for i in range(12):
        for j in range(12):
            if carte[i][j] == MUR: ligne.append('#')
            elif carte[i][j] == VIDE: ligne.append(' ')
            elif carte[i][j] == CAISSE: ligne.append('$')
            elif carte[i][j] == OBJECTIF: ligne.append('.')
            elif carte[i][j] == MARIO: ligne.append('@')
            elif carte[i][j] == CAISSE_OK: ligne.append('*')
        ligne.append('\n')
    f.write(''.join(ligne))

    f.close()

def searchMario(carte, joueurPos):      # Recherche de Mario
    for lgn in range(NB_BLOCS_HAUTEUR):             # et mise à jour de
        for col in range(NB_BLOCS_LARGEUR):          # ses coordonnées
            if carte[lgn][col] == MARIO:
                joueurPos.x = col
                joueurPos.y = lgn
                carte[lgn][col] = VIDE              # et vide sa case
    return

import pygame, time
from pygame.locals import *

from constantes import *
from fichiers import *
from general import *
from credits import *
from Astar import *
from globales import *
from loadSave import *
from aide import *

def jouer(screen, levelNumber, lang, langu, levelFinal, difficulty, soundly, mode):

# ---------- Variables locales à jouer() ---------------------------------

    boucle = True

    moveNumber = 0
    nombreDeVie = 3
    minutes = 0
    secondes = 0
    tempsPrecedent = 0
    perdu = False
    joueurPos = pygame.Rect(0,0,0,0)
    joueurPosPreced = ()
    listPos = []

    objectPos = pygame.Rect(0,0,0,0)
    marche = False
    nMarch = 0
    moveNumber = 0
    niveauAtteint = 1

    carte = [[int for lgn in range(NB_BLOCS_HAUTEUR)]for col in range(NB_BLOCS_LARGEUR)]
    copieCarte = [[int for lgn in range(NB_BLOCS_HAUTEUR)]for col in range(NB_BLOCS_LARGEUR)]

    # load images
    mur = pygame.image.load(SOURCE_IMG + 'mur.jpg').convert()
    caisse = pygame.image.load(SOURCE_IMG + 'caisse.jpg').convert()
    caisse_ok = pygame.image.load(SOURCE_IMG + 'caisse_ok.jpg').convert()
    objectif = pygame.image.load(SOURCE_IMG + 'objectif.png').convert_alpha()
    mario[HAUT] = pygame.image.load(SOURCE_IMG + 'mario_haut.gif').convert_alpha()
    mario[DROITE] = pygame.image.load(SOURCE_IMG + 'mario_droite.gif').convert_alpha()
    mario[BAS] = pygame.image.load(SOURCE_IMG + 'mario_bas.gif').convert_alpha()
    mario[GAUCHE] = pygame.image.load(SOURCE_IMG + 'mario_gauche.gif').convert_alpha()
    marioActuel = mario[BAS]

    # load sound
    pas = pygame.mixer.Sound('stepwlk2.wav')
    musique = pygame.mixer.Sound('mario.wav')

# ---------- Initialisations & chargements -------------------------------
    if difficulty:
        minutes, secondes = backTime(levelNumber, minutes, secondes)

    if soundly:
        musique.play(-1)
        musique.set_volume(0.25)
    # else:
    #     musique.stop()

    # load map
    chargeCarte(carte, levelNumber)

    # codage du tableau pour déplacements automatiques
    tableauCodeAStar(carte)

    # cherche mario --> joueurPos.x et joueurPos.y et VIDE sa position dans carte
    searchMario(carte, joueurPos)

    # white Bar
    whiteBar = pygame.Surface((screen.get_width(), 60), screen.get_flags())
    whiteBar.fill(WHITE)

    # timeText
    tempsActuel = pygame.time.get_ticks()

    pathFile = printLang(lang)                          # 'fr' ou 'en'
    sourceFile = SOURCE_FILE + pathFile + '/jeu.lvl'    # './files/' 'fr ou en' '/jeu.lvl'
    # Fin du Jeu! PERDU! BRAVO! Temps Aide: A Vies: Vie: Niveau Pas
    # ou
    # Game Over! LOSE! NICE! Time Help: H Lives: Life: Level Move
    lignes = compteLignes(sourceFile)
    tableau = [Text() for i in range(lignes)]   # remplit le tableau de jeu avec les mots de la langue
    initialiseGameTable(sourceFile, lignes, tableau)

    for i in range(2):      # coord du tableau 0 et 1 Fin du Jeu! PERDU! ou Game Over! LOSE!
        tableau[i].positionX = (screen.get_width() - tableau[i].partie.get_width())//2
        tableau[i].positionY = (screen.get_height() - tableau[i].partie.get_height())//2

    # timeText
    charTemps = tableau[3].data + ': ' + str(minutes) + ' : ' + str(secondes)
    pygame.font.init()
    police = pygame.font.Font('angelina.ttf', 20)
    tempsText = police.render(charTemps, True, GRAY, BLACK)

# ---------- Boucle principale du jeu ------------------------------------

    while boucle:

        for event in pygame.event.get():

            if soundly == False and pygame.mixer.get_busy():    # si le son fonctinne on l'arrête
                pygame.mixer.stop()

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                boucle = False      # sortie de la boucle

# ---------- prise en charge des actions de la souris pour jouer ------------------------------------------------------

            if event.type == MOUSEBUTTONDOWN:
                mousex,  mousey = event.pos     # coord x,y ecran
                caselgn, casecol = getCoordCaseJeu (mousex,  mousey) # x,y des cases du jeu

                # si dans zone d'affichage hors zone de jeu
                if caselgn > NB_CASES-1 or casecol > NB_CASES-1:
                    continue
                
                # copie de la carte du jeu
                for lgn in range(NB_BLOCS_HAUTEUR):
                    for col in range(NB_BLOCS_LARGEUR):
                        copieCarte[lgn][col] = carte[lgn][col]

                # clic sur case vide ou objectif
                if (carte[caselgn][casecol] == VIDE or carte[caselgn][casecol] == OBJECTIF):
                    # si clic sur perso
                    if (caselgn == joueurPos.y and casecol == joueurPos.x): break
                        # and (caselgn != joueurPos.y or casecol != joueurPos.x):
                    tableauCodeAStar(carte)
                    trajet[:] = []
                    Ast.entreey, Ast.entreex = joueurPos.x, joueurPos.y
                    Ast.sortiex = caselgn
                    Ast.sortiey = casecol
                    grille[Ast.entreex][Ast.entreey] = 3	# Definit l'etat de l'entree
                    grille[Ast.sortiex][Ast.sortiey] = 4 	# Definit l'etat de la sortie
                    w = AStar()     # determine le chemin
                    w.process()

                    #si trajet d'une seule case
                    if len(trajet) == 0 \
                    and (abs(Ast.sortiex - Ast.entreex) == 1 and Ast.entreey == Ast.sortiey)\
                    or (abs(Ast.sortiey - Ast.entreey) == 1 and Ast.entreex == Ast.sortiex):
                        if carte[Ast.sortiex][Ast.sortiey] == VIDE\
                        or carte[Ast.sortiex][Ast.sortiey] == OBJECTIF:
                            # on valide affichage perso
                            trajet.append((Ast.sortiex, Ast.sortiey))
                            trajet.reverse()
                            marche = True
                            nMarch = len(trajet)
                            
                    # si trajet de plus d'une case
                    elif len(trajet) > 0:
                        # on affiche perso
                        trajet.append((Ast.sortiex, Ast.sortiey))
                        trajet.reverse()
                        marche = True
                        joueurPosPreced = (joueurPos.x, joueurPos.y)
                        nMarch = len(trajet)

                elif (carte[caselgn][casecol] == CAISSE or carte[caselgn][casecol] == CAISSE_OK)\
                      and (abs(caselgn - joueurPos.y) == 1 or abs(casecol - joueurPos.x) == 1):
                    # clique case autre que vide ou objectif
                    persocol, persolgn =  joueurPos.x, joueurPos.y
                    joueurPosPreced = (joueurPos.x, joueurPos.y)
                    listPos.append(joueurPosPreced)
                    if caselgn < persolgn and casecol == persocol:
                        marioActuel = mario[HAUT]
                        deplacement(carte, persolgn, persocol, HAUT, joueurPos, joueurPosPreced)
                        tableauCodeAStar(carte)
                        moveNumber += 1
                        if soundly == True: pas.play()
                    elif caselgn > persolgn and casecol == persocol:
                        marioActuel = mario[BAS]
                        deplacement(carte, persolgn, persocol, BAS, joueurPos, joueurPosPreced)
                        tableauCodeAStar(carte)
                        moveNumber += 1
                        if soundly == True: pas.play()
                    elif casecol < persocol and caselgn == persolgn:
                        marioActuel = mario[GAUCHE]
                        deplacement(carte, persolgn, persocol, GAUCHE, joueurPos, joueurPosPreced)
                        tableauCodeAStar(carte)
                        moveNumber += 1
                        if soundly == True: pas.play()
                    elif casecol > persocol and caselgn == persolgn:
                        marioActuel = mario[DROITE]
                        deplacement(carte, persolgn, persocol, DROITE, joueurPos, joueurPosPreced)
                        tableauCodeAStar(carte)
                        moveNumber += 1
                        if soundly == True: pas.play()

# ---------- prise en charge des touches spéciales: reour arrière, niveau suivant.... ---------------------------------

            elif event.type == KEYDOWN:

                # Retour en arrière d'une position
                if event.key == K_F1:
                    joueurPos.x, joueurPos.y = joueurPosPreced
                    for lgn in range(NB_BLOCS_HAUTEUR):
                        for col in range(NB_BLOCS_LARGEUR):
                            carte[lgn][col] = copieCarte[lgn][col]
                    pygame.time.delay(250)

                # retour debut du même niveau
                if event.key == K_F2:
                    if difficulty:
                        minutes, secondes = backTime(levelNumber, minutes, secondes)
                    else:
                        minutes = 0
                        secondes = 0
                        moveNumber = 0
                    marioActuel = mario[BAS]
                    chargeCarte(carte, levelNumber)
                    searchMario(carte, joueurPos)
                    pygame.time.delay(250)

                # Passage au niveau suivant
                elif event.key == K_PAGEUP:
                    if levelNumber > 1:
                        levelNumber -= 1
                        if difficulty:
                            backTime(levelNumber,minutes,secondes)
                        else:
                            minutes=0
                            secondes=0
                            moveNumber=0
                        marioActuel=mario[BAS]
                        chargeCarte(carte,levelNumber)
                        searchMario(carte, joueurPos)

                # Retour niveau precedent
                elif event.key == K_PAGEDOWN:
                    if levelNumber < niveauAtteint:
                        levelNumber += 1
                        if difficulty:
                            backTime(levelNumber,minutes,secondes)
                        else:
                            minutes=0
                            secondes=0
                            moveNumber=0
                        marioActuel=mario[BAS]
                        chargeCarte(carte,levelNumber)
                        searchMario(carte, joueurPos)

                # sauvegarde du niveau courant
                elif event.key == K_s:
                    saveNumber=1
                    loadSaveMenu(screen,levelNumber,saveNumber,carte, joueurPos,levelFinal)

                # chargement du niveau sauvegardé
                elif event.key == K_l:
                    saveNumber=0
                    levelNumber = loadSaveMenu(screen,levelNumber,saveNumber,carte, joueurPos,levelFinal)
                    niveauAtteint=levelNumber

                # On obtient de l'aide en appuyant sur A(ide) en FR et sur H(elp) en EN
                elif event.key == K_a and lang == FR:
                    aide(screen,mode,lang,langu)

                elif event.key == K_h and lang == EN:
                    aide(screen,mode,lang,langu)

# ---------- Affiche les résultats des actions précédentes ----------------------------------------------------------

        # Ecran noir --> efface fenetre
        screen.fill(BLACK)

        # Affiche tous les éléments sauf Mario
        objectifRestant = 0
        for lgn in range(NB_BLOCS_LARGEUR):
            for col in range(NB_BLOCS_HAUTEUR):
                objectPos.x = col * TAILLE_BLOC
                objectPos.y = lgn * TAILLE_BLOC
                if carte[lgn][col] == MUR:
                    screen.blit(mur, objectPos)
                    continue
                if carte[lgn][col] == CAISSE:
                    screen.blit(caisse, objectPos)
                    continue
                if carte[lgn][col] == CAISSE_OK:
                    screen.blit(caisse_ok, objectPos)
                    continue
                if carte[lgn][col] == OBJECTIF:
                    objectifRestant = 1 # On vérifie s'il reste au moins 1 objectif
                    screen.blit(objectif, objectPos)
                    continue

        # Déplacements de Mario
        if marche:
            m = persoVersCase(nMarch, joueurPos, joueurPosPreced)
            marioActuel = mario[m]
            objectPos.x = joueurPos.x * TAILLE_BLOC
            objectPos.y = joueurPos.y * TAILLE_BLOC
            screen.blit(marioActuel, objectPos)
            moveNumber += 1
            nMarch -= 1
            if soundly == True: pas.play()
            time.sleep(.250)
            if nMarch <= 0:
                marche = False
                trajet[:] = []
                tableauCodeAStar(carte)
        else:
            # Affiche Mario d'après ses coord joueurPos.x & y
            objectPos.x = joueurPos.x  * TAILLE_BLOC
            objectPos.y = joueurPos.y * TAILLE_BLOC
            screen.blit(marioActuel, objectPos)
#            listPos.append(joueurPosPreced)     #----------------------------------------------------------
#            print(joueurPosPreced)
#            print(listPos)


        # Si tous les objectifs sont recouverts
        if objectifRestant == 0:        # Affiche le texte Bravo! ou Nice!
            police = pygame.font.Font('angelina.ttf', 80)
            police.set_bold(True)
            objectPos.x = (screen.get_width() - tableau[2].partie.get_width())//2
            objectPos.y = (screen.get_width() - tableau[2].partie.get_height())//2
            screen.blit(tableau[2].partie, objectPos)

        police.set_bold(False)
        police = pygame.font.Font('angelina.ttf', 20)

        # Affichage de la bande blanche du bas
        objectPos.x = 0
        objectPos.y = screen.get_height() - whiteBar.get_height()
        screen.blit(whiteBar, objectPos)

        # Affichage du niveau
        levelNumero = tableau[7].data + ' : ' + str(levelNumber)  # texte à afficher
        levelText = police.render(levelNumero, True, GRAY)        # conversion en surface
        objectPos.x = 10                                          # coordonnées
        objectPos.y = (screen.get_height() - whiteBar.get_height()) + 5
        screen.blit(levelText, objectPos)                         # blitage à l'écran

        # Affichage du nombre de Pas
        moveNumero = tableau[8].data + ' : ' + str(moveNumber)  # texte à afficher
        moveText = police.render(moveNumero, True, GRAY)        # conversion en surface
        objectPos.x = 120                       # coordonnées y est inchangé
        screen.blit(moveText, objectPos)        # blitage à l'écran

        # Affichage du Temps
        objectPos.x = 220
        tempsActuel = pygame.time.get_ticks()

        if tempsActuel - tempsPrecedent >= 1000:        # 1000 ms = 1 seconde
            if difficulty:
                secondes -= 1
                if secondes == 0 and minutes > 0:
                    minutes -= 1
                    secondes = 59
            else:
                secondes += 1                               # 1 seconde de plus
                if secondes == 60:                          # 60s = 1mn 0s
                    minutes += 1
                    secondes = 0
                                                        # ce qui sera affiché
            charTemps = tableau[3].data + ' : ' + str(minutes) + ' : ' + str(secondes)

            if difficulty and minutes == 0 and secondes == 1:   # si Contre le temps et reste 1s
                police = pygame.font.Font('angelina.ttf', 80)
                police.set_bold(True)
                if nombreDeVie == 1:
                    screen.blit(tableau[0].partie, (tableau[0].positionX, tableau[0].positionY))
                    levelNumber = 1
                else:
                    screen.blit(tableau[1].partie, (tableau[1].positionX, tableau[1].positionY))
                perdu = True
                nombreDeVie -= 1

            police = pygame.font.Font('angelina.ttf', 20)
            tempsText = police.render(charTemps, True, GRAY) # conversion en surface
            tempsPrecedent = tempsActuel        # nouveau temps

        screen.blit(tempsText, objectPos)   # Affiche Temps: .. mn ..s

        # helpText
        objectPos.x = 350
        screen.blit(tableau[4].partie, objectPos)

        # vie text
        if difficulty:
            objectPos.x = 10
            objectPos.y = (screen.get_height() - tableau[5].partie.get_height())-10
            if nombreDeVie > 1:
                screen.blit(tableau[5].partie, objectPos)
            else:
                screen.blit(tableau[6].partie, objectPos)
            objectPos.x = 15 + tableau[5].partie.get_width()
            objectPos.y = (screen.get_height() - tableau[5].partie.get_height()) - 20
            for i in range(nombreDeVie):
                screen.blit(mario[BAS], objectPos)
                objectPos.x += 25

        # mise a jour affichage de l'écran ---------------------
        pygame.display.flip()

# ---------- Fin de tableau perdu ou gagné ----------------------------------------------------------------------------

        if perdu:       # si temps écoulé en cas de lutte contre le chrono
            if nombreDeVie == 0:
                boucle = False
            pygame.time.delay(2000)
            if difficulty:
                minutes, secondes = backTime(levelNumber, minutes, secondes)
            else:
                # Remise a zero des compteurs
                minutes[0] = 0
                secondes[0] = 0
            moveNumber = 0
            # search mario
            marioActuel = mario[BAS]
            # load next level
            chargeCarte(carte, levelNumber)
            # get mario new position
            searchMario(carte, joueurPos)
            pygame.display.flip()
            perdu = False

        if objectifRestant == 0:        # si on a gagné le niveau
            pygame.time.delay(2000)
            levelNumber += 1
            saveNumber=2
            levelNumber = loadSaveMenu(screen,levelNumber,saveNumber,carte,joueurPos,levelFinal)
            if levelNumber > levelFinal:
                boucle = False
                credits(screen,lang, levelNumber)   # --> on a atteint le dernier niveau
            niveauAtteint = levelNumber
            if difficulty:
                minutes, secondes = backTime(levelNumber, minutes, secondes)
            else:
                # Remise a zero des compteurs
                minutes = 0
                secondes = 0

            moveNumber = 0          # RAZ du nombre de pas

            joueurPosPreced = []    # Raz ancienne position

            # search mario
            marioActuel = mario[BAS]

            # load next level
            chargeCarte(carte, levelNumber)

            # get mario new position
            searchMario(carte, joueurPos)

            pygame.event.clear()
            pygame.display.flip()       # mise a jour ecran

# ---------- Fonctions locales -------------------------------------------

def direction(xdeb,  ydeb, xarriv, yarriv):
    """Choix du perso a afficher en fonction de la direction du deplacement"""
    if yarriv - ydeb > 0:       # si arrivee > depart verticalement
        marioActuel = mario[BAS]               # => deplacement vers le bas
        m = BAS
    elif yarriv - ydeb < 0:     # si arrivee < depart verticalement
        marioActuel = mario[HAUT]              # => deplacement vers le haut
        m = HAUT
    elif xarriv - xdeb > 0:     # si arrivee > depart horizontalement
        marioActuel = mario[DROITE]            # => deplacement vers la droite
        m = DROITE
    elif xarriv - xdeb < 0:     # si arrivee > depart horizontalement
        marioActuel = mario[GAUCHE]             # => deplacement vers la gauche
        m = GAUCHE
    return m

def persoVersCase(nMarch, joueurPos, joueurPosPreced):
    """Parcours de la pos actuelle a pos case vide cliquee de coord cx, cy"""
    xav, yav = joueurPos.x, joueurPos.y
    yp, xp = trajet[nMarch - 1]                          # coord pos case ecran dest
    m = direction(xav, yav, xp, yp)     # choix perso
    joueurPos.x, joueurPos.y = xp, yp
    return m

def getCoordCaseJeu (mousex,  mousey):
    """Coord ecran pixel --> coord case ecran"""
    casey = (mousex // TAILLE_BLOC)
    casex = (mousey // TAILLE_BLOC)
    return (casex, casey)

#def searchMario(carte, joueurPos):      # Recherche de Mario
#    for lgn in range(NB_BLOCS_HAUTEUR):             # et mise à jour de
#        for col in range(NB_BLOCS_LARGEUR):          # ses coordonnées
#            if carte[lgn][col] == MARIO:
#                joueurPos.x = col
#                joueurPos.y = lgn
#                carte[lgn][col] = VIDE              # et vide sa case
#    return

def deplacement(carte, poslgn, poscol, direction, joueurPos, joueurPosPreced):

#    joueurPosPreced = (joueurPos.x, joueurPos.y)
#    listPos.append(joueurPosPreced)

    if direction == HAUT:
        if poslgn - 1 < 0:      # Si le joueur depasse l'ecran, on arrete
            return False   # retourne False si pas de mouvement

        if carte[poslgn-2][poscol] == MUR:   # S'il y a un mur, on arrete
            return False    # retourne False si pas de mouvement

        # Si on veut pousser une caisse, il faut verifier qu'il n'y a pas de mur derriere (ou une autre caisse, ou la limite du monde)
        if ((carte[poslgn - 1][poscol] == CAISSE or carte[poslgn - 1][poscol] == CAISSE_OK) \
            and (poslgn - 2  < 0 or carte[poslgn - 2][poscol] == MUR or \
            carte[poslgn - 2][poscol] == CAISSE or carte[poslgn - 2][poscol] == CAISSE_OK)):
            return False    # retourne False si pas de mouvement
        # Si on arrive la, c'est qu'on peut deplacer le joueur !
        # On verifie d'abord s'il y a une caisse a deplacer

        if carte[poslgn - 1][poscol] == CAISSE \
        or carte[poslgn - 1][poscol] == CAISSE_OK:    # si caisse, on la deplace
            deplacerCaisse(carte, poslgn-1, poscol, poslgn-2, poscol)

        joueurPos.y -= 1      # On peut enfin faire monter le joueur (oufff !)

    if direction == BAS:
        if poslgn + 1 >= NB_BLOCS_HAUTEUR:
            return False    # retourne False si pas de mouvement

        if carte[poslgn + 2][poscol] == MUR:
            return False    # retourne False si pas de mouvement

        if ((carte[poslgn + 1][poscol] == CAISSE or carte[poslgn + 1][poscol] == CAISSE_OK) \
            and (poslgn + 2 >= NB_BLOCS_HAUTEUR or carte[poslgn + 2][poscol] == CAISSE_OK \
            or carte[poslgn + 2][poscol] == CAISSE or carte[poslgn + 2][poscol] == CAISSE_OK)):
            return False            # retourne si pas de mouvement

        if carte[poslgn + 1][poscol] == CAISSE \
        or carte[poslgn + 1][poscol] == CAISSE_OK:    # caisse ou caisseok
            deplacerCaisse(carte, poslgn + 1, poscol, poslgn + 2, poscol)

        joueurPos.y += 1

    if direction == GAUCHE:
        if poslgn - 1 < 0:
            return False    # retourne False si pas de mouvement

        if carte[poslgn][poscol - 2] == MUR:
            return False     # retourne False si pas de mouvement

        if ((carte[poslgn][poscol - 1] == CAISSE or carte[poslgn][poscol - 1] == CAISSE_OK) \
            and (poscol - 2 < 0 or carte[poslgn][poscol - 2] == MUR \
            or carte[poslgn][poscol - 2] == CAISSE or carte[poslgn][poscol - 2] == CAISSE_OK)):
            return                      # retourne si pas de mouvement

        if carte[poslgn][poscol - 1] == CAISSE \
        or carte[poslgn][poscol - 1] == CAISSE_OK:       # caisse ou caisseok
            deplacerCaisse(carte, poslgn, poscol - 1, poslgn, poscol - 2)

        joueurPos.x -= 1

    if direction == DROITE:
        if poslgn + 1 >= NB_BLOCS_LARGEUR:   # hors fenetre a droite
            return False    # retourne False si pas de mouvement

        if carte[poslgn][poscol + 2] == MUR:  # mur a droite
            return False    # retourne False si pas de mouvement

        if ((carte[poslgn][poscol + 1] == CAISSE or carte[poslgn][poscol + 1] == CAISSE_OK)
            and (poscol + 2 >= NB_BLOCS_LARGEUR or carte[poslgn][poscol + 2] == MUR or
             carte[poslgn][poscol + 2] == CAISSE or carte[poslgn][poscol + 2] == CAISSE_OK)):
            return                  # retourne si pas de mouvement

        if carte[poslgn][poscol + 1] == CAISSE or carte[poslgn][poscol + 1] == CAISSE_OK:
            deplacerCaisse(carte, poslgn, poscol + 1, poslgn, poscol + 2)

        joueurPos.x += 1
    return True         # retourne Vrai si un mouvement a eu lieu

def deplacerCaisse(carte, premiereCaseX, premiereCaseY, secondeCaseX, secondeCaseY):

    if carte[secondeCaseX][secondeCaseY] == OBJECTIF:
        carte[secondeCaseX][secondeCaseY] = CAISSE_OK
    else:
        carte[secondeCaseX][secondeCaseY] = CAISSE

    if carte[premiereCaseX][premiereCaseY] == CAISSE_OK:
        carte[premiereCaseX][premiereCaseY] = OBJECTIF
    else:
        carte[premiereCaseX][premiereCaseY] = VIDE

def backTime(levelNumber, min, sec):
    if levelNumber == 1:        # niveau 1 --> 10 secondes pour le jeu
        min = 0
        sec = 10

    elif levelNumber == 2:      # niveau 2 --> 2 mn 1 sec  pour le jeu
        min = 2
        sec = 1

    elif levelNumber == 3:      # niveau 3 --> 5 mn 1 sec  pour le jeu
        min = 5
        sec = 1

    else:               # niveaux suivants --> 10 mn 1 sec  pour le jeu
        min = 10
        sec = 1
    return min, sec

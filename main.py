"""Le module responsable de l'affichage"""

"""Import des packages/biblios"""
import pygame as p
# chessEngine est le moteur responsable du respect des lois du jeu d'échec
import ChessEngine
# utiliser pour éliminer les doublets dans une liste
from collections import OrderedDict
# menu de promotion au cas de promotion d'un pion
from promotion import promotion
# classe pour récupérer les coordonnées des mouvements
from Move import Move
# AI au cas PvAI
from MoveFinder import *

"""Les variables globales"""
# Dimension de la fenêtre
WIDTH = 720

# la Dimension de l'échiquier
DIMENSION = 8

# la taille d'un carré
SQ_SIZE = WIDTH // DIMENSION

# Le nombre de frame par seconde, nombre du "re-dessin" du contenu de la fenêtre
FPS = 60

# Dictionnaire de stockage des images des pieces, preferable de les stocker comme variable, afinRa d'éviter les lags
IMAGES = {}

# Liste des pieces
PIECES = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]

"""Les fonctions"""


# fonction qui associe les images aux pièces correspondantes
def load_images(img):
    for piece in PIECES:
        # transform.smoothscale adapte l'image à la taille des cases de l'échiquier
        img[piece] = p.transform.smoothscale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


# utiliser au cas où l'utilisateur veut jouer avec les pièces noires
def load_reverse_images(img):
    for piece in PIECES:
        if piece[0] == "w":
            img["b" + piece[1]] = p.transform.smoothscale(p.image.load(f"./images/{piece}.png"), (SQ_SIZE, SQ_SIZE))
        else:
            img["w" + piece[1]] = p.transform.smoothscale(p.image.load(f"./images/{piece}.png"), (SQ_SIZE, SQ_SIZE))


# fonction d'affichage de l'échiquier
def drawBoard(window, is_black):
    global color
    # couleur on rgb
    light = (232, 235, 239)
    dark = (125, 135, 169)
    # list des couleurs de l'échiquier
    colors = [light, dark]

    # Insérer du texte
    FONT = p.font.Font(None, 27)

    # liste des lettres de marquages de colonnes
    alpha_list = ["a", "b", "c", "d", "e", "f", "g", "h"]
    # en renverse la liste des alphabets au cas du choix des pièces noires
    if is_black:
        alpha_list.reverse()

    # dessin des cases de l'échiquier
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            """si la case est d'indice pair sa couleur est "light" d'indice 0,alors que s'elle est impaire sa couleur 
            est "dark" d'indice "1" """

            color = colors[((r + c) % 2)]

            # dessin des carrés sous forme de rectangle
            # Rect(left, top, width, height)
            p.draw.rect(window, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

            """précise la couleur et la chaine à afficher on affiche la lettre en couleur opposée de la couleur de la 
            case, si la case est "light" la lettre est "dark" """

            alpha = FONT.render(alpha_list[c], True, colors[c % 2])

            # positionne l'alphabet dans la dernière ligne de l'échiquier
            # on commence de c+1 puisque le c initial est nul
            """la case c est la première case et c+1 est la 2ᵉ donc en retranche une partie de c+1 pour afficher la 
            lettre à la fin de la case d'avant"""
            window.blit(alpha, (SQ_SIZE * (c + 1) - (DIMENSION + 3), WIDTH - 19))

        # le numéro à afficher sur chaque ligne
        ligne = r + 1 if is_black else DIMENSION - r

        # positionne les nombres dans la première case de chaque colonne
        nbr = FONT.render(str(ligne), True, color)
        window.blit(nbr, (0, r * SQ_SIZE + 5))


# affichage des pièces
def drawPieces(window, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            # on affecte à chaque pièce sur liste son image correspondente des dictionnaires des images de pieces
            piece = board[r][c]
            if piece != "--":  # piece != d'une case vide
                """c * SQ_SIZE, r * SQ_SIZE marquent la position de la case sur laquelle le pièce est affichée, 
                SQ_SIZE, SQ_SIZE sont les dims de la case """
                window.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


# fonction de dessin/ mis-è-jour après chaque événement de l'écran
def drawState(window, gs, is_black, draw_move=None):
    # si des mouvements à dessiner sont valables elle ne contient rien par défaut
    if draw_move:
        draw_available_moves(window, draw_move)
    else:
        # dessine l'échiquier
        drawBoard(window, is_black)
        # surligne une pièce sélectionnée
        high_light_King(window, gs)
        # affiche les pièces
        drawPieces(window, gs.board)


# liste qui affiche les mouvements possibles de la pièce sélectionnée
def draw_available_moves(window, moveList):
    # moveList est la liste des mouvements
    for move in moveList:
        # if len(move) > 0:
        r = move[0]
        c = move[1]
        # (c * SQ_SIZE + SQ_SIZE // 2,r * SQ_SIZE + SQ_SIZE // 2) sont les coordonnées du centre du cercle
        # SQ_SIZE // 7 est le rayon du cercle
        p.draw.circle(window, (133, 193, 233), (c * SQ_SIZE + SQ_SIZE // 2, r * SQ_SIZE + SQ_SIZE // 2),
                      SQ_SIZE // 7)
        # p.display.update()


# fonction qui surligne d'une pièce sélectionnée
def high_light_piece(window, r, c, board):
    # on redessine la case avec une couleur différente
    p.draw.rect(window, (133, 193, 233), p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    # puis on redessine la pièce en dessus
    window.blit(IMAGES[board[r][c]], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.display.update()


# surligne le roi en cas d'échec
def high_light_King(window, gs):
    # juste en cas d'échec
    if gs.inCheck:
        if gs.whiteToMove:
            # les coordonnées du roi blanc en cas de son échec
            r = gs.whiteKinglocation[0]
            c = gs.whiteKinglocation[1]
        else:
            # les coordonnées du roi noir en cas de son échec
            r = gs.blackKinglocation[0]
            c = gs.blackKinglocation[1]
        RED = (255,0,0)
        # dessine une case rouge
        # p.draw.rect(window, RED, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

        # afficher une case transparente
        s = p.Surface((SQ_SIZE, SQ_SIZE))  # la taille de la case
        s.set_alpha(150)  # la case est plus transparente quand la valeur est plus petite
        s.fill(RED)  # this fills the entire surface
        window.blit(s, (c * SQ_SIZE, r * SQ_SIZE))


# affichage d'un texte à la fin du jeu
def end_game_text(window, text):
    # prend l'écran entier
    s = p.Surface((WIDTH, WIDTH))
    # alpha pour la transparence
    s.set_alpha(100)
    # la couleur de l'arrière-plan
    s.fill((200, 200, 200))
    # affichage d'un écran gris transparent
    window.blit(s, (0, 0))
    # font du texte qui sera afficher
    FONT = p.font.Font(None, 70)
    TEXT = FONT.render(text, True, p.Color("Black"))
    # position du texte sur l'écran, move est responsable de le positionner
    # WIDTH // 3 le positionne par rapport à la longueur
    # WIDTH // 2 - TEXT.get_width() // 2 le positionne par rapport à la largeur
    # get_width retourne la largeur en pixel du texte à afficher
    textLocation = p.Rect(0, 0, WIDTH, WIDTH).move(WIDTH // 2 - TEXT.get_width() // 2, WIDTH // 3)
    window.blit(TEXT, textLocation)

    # affiche des options à faire après la fin du jeu
    FONT = p.font.Font(None, 40)
    TEXT = FONT.render("R to Reset", True, p.Color("Black"))
    textLocation = p.Rect(0, 0, WIDTH, WIDTH).move(WIDTH // 2 - TEXT.get_width() // 2, WIDTH // 2)
    window.blit(TEXT, textLocation)

    # afficher la possibilité de retourner au menu d'accueille
    FONT = p.font.Font(None, 40)
    TEXT = FONT.render("A - Return to Menu", True, p.Color("Black"))
    textLocation = p.Rect(0, 0, WIDTH, WIDTH).move(WIDTH // 2 - TEXT.get_width() // 2, (WIDTH//2)+50)
    window.blit(TEXT, textLocation)


def get_draw_move(valid_moves, startSq, draw_move):
    for moves in valid_moves:
        if moves.startSq == startSq:
            draw_move.append(moves.endSq)
    draw_move = list(OrderedDict.fromkeys(draw_move))
    return draw_move


def reset(gs):
    while gs.moveLog:
        gs.undoMove()
    gs.checkMate = False
    gs.staleMate = False


"""Fonction définissant une partie d'échec"""


def main(mode=True, is_black=False):
    # initialisation des modules de pygame
    p.init()
    # variable pour stocker les mouvements à dessiner
    global draw_moves
    draw_moves = []
    # fonction qui associe à chaque piece son image
    load_images(IMAGES)
    # La fenetre elle-meme
    WIN = p.display.set_mode((WIDTH, WIDTH))
    # Afficher "Chess game" dans la barre de la fenêtre
    p.display.set_caption("Chess Game")

    # variable utiliser pour la FPS/ nombre de fois le contenu affiché est dessiné/seconde
    clock = p.time.Clock()

    # objet de class gameState
    gs = ChessEngine.gameState()
    # liste contenant tous les mouvements possibles dans une partie
    valid_moves = gs.getValidMoves()

    # flag pour génerer des nouveaux mvts juste au cas le joueur a effectué un mvts valide
    moveMade = False

    # constante de la boucle responsable de l'affichage de la fenêtre
    run = True

    # historique des cliques
    sqSelected = ()  # va prendre la ligne et la colonne de la case choisie
    playerClicks = []  # va contenir la position initial et terminal de la piece

    # les joueurs
    if mode:
        # mode PvP
        playerOne = True  # True si le joueur est humain / False s'il n'est pas
        playerTwo = True
    else:
        # mode PvAI
        playerOne = False  # True si le joueur est humain / False s'il n'est pas
        playerTwo = False
        # cas où l'utilisateur choisit de jouer avec les pièces noires
        if is_black:
            # pour choisir noir/blanc
            gs.whiteToMove = False
            load_reverse_images(IMAGES)
            valid_moves = gs.getValidMoves()

    # variable indiquant la fin d'une partie
    game_over = False
    # boucle principale
    while run:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        clock.tick(FPS)
        # responsable de l'ouverture et fermeture de la fenêtre
        for event in p.event.get():
            if event.type == p.QUIT:
                run = False
            # gestion des cliques souris
            elif event.type == p.MOUSEBUTTONDOWN:
                # si l'utilisateur clique sur le bouton gauche
                if p.mouse.get_pressed()[0]:
                    # si le jeu n'est pas terminé et le joueur est humain
                    if not game_over and humanTurn:
                        # la position de la souris (colonne, ligne) sur l'échiquier
                        location = p.mouse.get_pos()
                        col = location[0] // SQ_SIZE  # colonne de l'échiquier
                        row = location[1] // SQ_SIZE  # ligne de l'échiquier

                        # surligner la case de la piece choisie
                        if gs.board[row][col] != "--":
                            high_light_piece(WIN, row, col, gs.board)
                            # afficher les mouvements possibles
                        get_draw_move(valid_moves, (row, col), draw_moves)
                        # clique sur une piece qui ne peut pas bouger
                        if draw_moves:
                            # cas où le joueur clique sur la même piece deux fois
                            if sqSelected == (row, col):
                                sqSelected = ()
                                playerClicks = []
                                draw_moves = []
                            else:
                                sqSelected = (row, col)
                                playerClicks.append(sqSelected)
                                # cas de sélection d'une case vide comme case de depart
                                if gs.board[playerClicks[0][0]][playerClicks[0][1]] == "--":
                                    sqSelected = ()
                                    playerClicks = []
                            # les deux cliques de départ et d'arrivée sont valides
                            if len(playerClicks) == 2:  # responsable du déplacement des pieces
                                # réception des cases choisies par le joueur
                                move = Move(playerClicks[0], playerClicks[1], gs.board)
                                # réalisation du mouvement
                                for i in range(len(valid_moves)):
                                    if move == valid_moves[i]:
                                        # s'il s'agit d'un pion à promouvoir
                                        if move.isPawnPromotion:
                                            gs.piece_promo = promotion(move.endRow, move.endCol)

                                        # réaliser un mouvement
                                        gs.makeMove(valid_moves[i])
                                        print(move.getChessNotation())
                                        moveMade = True
                                    # vider les variables qui recevant les cliques
                                    sqSelected = ()
                                    playerClicks = []
                                    draw_moves = []

            # annulation d'un mouvement
            elif event.type == p.KEYDOWN:
                if event.key == p.K_z:
                    gs.undoMove()
                    gs.checkMate = False
                    gs.staleMate = False
                    game_over = False
                    moveMade = True
                # reset le jeu
                elif event.key == p.K_r and game_over:
                    # draw_moves = []
                    # sqSelected = ()
                    # playerClicks = []
                    game_over = False
                    # moveMade = True
                    reset(gs)
                    humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
                    valid_moves = gs.getValidMoves()
                    # return

                elif event.key == p.K_a and game_over:
                    return

        # mouvements au cas joueurs vs AI
        if not game_over and not humanTurn:
            AI_move = findBestMove(gs, valid_moves)
            # au cas où le AI ne trouve aucun mouvement possible
            if not AI_move:
                AI_move = findRandomMove(valid_moves)
            gs.makeMove(AI_move)
            print(AI_move.getChessNotation())
            moveMade = True
        # si un mouvement est réalisé, on régénère une nouvelle liste de mouvements
        if moveMade:
            valid_moves = gs.getValidMoves()
            moveMade = False

        # on redessine le contenu de l'écran après les modifications
        drawState(WIN, gs, is_black, draw_moves)
        # cas d'un échec-et-mat
        if gs.checkMate:
            # le jeu se termine
            game_over = True
            # puisque la fonction makeMove change le trait après son appelle, le dernier joueur qui a le trait
            # est celui qui a perdu
            if gs.whiteToMove:
                endText1 = "White wins" if is_black else "Black wins"
                end_game_text(WIN, endText1)
            else:
                endText2 = "Black wins" if is_black else "White wins"
                end_game_text(WIN, endText2)
        elif gs.staleMate:
            game_over = True
            end_game_text(WIN, "Stalemate")

        p.display.flip()

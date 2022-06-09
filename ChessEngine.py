"""Pour l'instant, responsable du stockage de l'historique des mouvements aka l'état courant du jeu
et la vérification de la légitimité des mouvements des pieces"""
from piece import *
from Move import *
from castleRights import *


class gameState:
    """ Board : attribut representant m'état courant(ici initial) de l'échiquier
        Couleur : b =noir , w= blanc
        piece : R = tour , N=Cavalier, B=Fou, Q=Dame, K=Roi, P=pion
        "--" represente une case vide, utiliser au lieu d"un zero afin de faciliter l'échange de str par str"""

    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        # self.board = [
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "bQ", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "wK", "--", "--", "--"]
        # ]
        # self.board =[
        #              ['--', '--', 'wQ', '--', '--', 'bB', 'bN', 'bR'],
        #              ['--', '--', '--', '--', 'bP', '--', 'bP', 'bQ'],
        #              ['--', '--', '--', '--', '--', 'bP', 'bK', 'bR'],
        #              ['--', '--', '--', '--', '--', '--', '--', 'bP'],
        #              ['--', '--', '--', '--', '--', '--', '--', 'wP'],
        #              ['--', '--', '--', '--', 'wP', '--', '--', '--'],
        #              ['wP', 'wP', 'wP', 'wP', '--', 'wP', 'wP', '--'],
        #              ['wR', 'wN', 'wB', '--', 'wK', 'wB', 'wN', 'wR']]

        # self.board =[['--', 'bN', '--', 'bK', '--', 'bB', 'bN', 'bR'], ['--', '--', '--', '--', 'bP', '--', '--', '--'], ['--', '--', 'bP', 'bP', '--', 'bP', 'wQ', '--'], ['--', 'bP', '--', '--', '--', '--', '--', '--'], ['--', 'bP', 'bR', '--', '--', '--', '--', '--'], ['--', '--', '--', '--', '--', '--', 'bP', 'bB'], ['--', '--', '--', '--', '--', '--', '--', '--'], ['--', '--', '--', '--', 'wK', '--', '--', '--']]

        # self.board = [
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "wB", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"]
        # ]
        self.moveFunction = {"P": self.get_Pawn_moves,
                             "Q": self.get_Queen_moves,
                             "K": self.get_King_moves,
                             "N": self.get_Knight_moves,
                             "B": self.get_Bishop_moves,
                             "R": self.get_Rook_moves}

        """True : Blanc a le trait; False: Noir a le trait, initialiser à True car le blanc commence le premier """
        self.whiteToMove = True
        """L'historique des mvts"""
        self.moveLog = []
        # *****************************************************************************************************************************************************************************
        self.whiteKinglocation = (7, 4)
        self.blackKinglocation = (0, 4)
        # *****************************************************************************************************************************************************************************
        self.endGame = False
        self.pieces_left = []
        self.checkMate = False
        self.staleMate = False
        self.inCheck = False  # si un roi est en échec cette variable devient vraie
        self.pins = []  # pieces bloquées afin de protéger le roi
        self.checks = []  # pièces qui mettent le roi en échec
        # *****************************************************************************************************************************************************************************
        self.piece_promo = "Q"
        # *****************************************************************************************************************************************************************************
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [
            CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs,
                         self.currentCastlingRight.bqs)]

    # *****************************************************************************************************************************************************************************
    # fonction responsable de déplacer une piece d'une case à une autre
    def makeMove(self, move):
        # vide la case de départ
        self.board[move.startRow][move.startCol] = "--"
        # déplace la pièce vers la case choisie
        self.board[move.endRow][move.endCol] = move.pieceMoved
        # change le trait
        self.whiteToMove = not self.whiteToMove
        # ajoute le mouvement au moveLog
        self.moveLog.append(move)
        # la mise-à-jour de la position du roi
        if move.pieceMoved == 'wK':
            self.whiteKinglocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKinglocation = (move.endRow, move.endCol)
        # promettre le pion en cas de promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + self.piece_promo

        # castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:  # kingside castle move
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]  # moves the rook
                self.board[move.endRow][move.endCol + 1] = '--'  # erase old rook
            else:  # queenside castle move
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]  # moves the rook
                self.board[move.endRow][move.endCol - 2] = "--"

        # mise à jour le roque si le roi ou la tour ont été deplacer
        self.updateCastleRights(move)
        # l'ajout des droits de roque dans la liste casteRightsLog
        self.castleRightsLog.append(
            CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs,
                         self.currentCastlingRight.bqs))

    # *****************************************************************************************************************************************************************************
    # pour annuler un mouvement
    def undoMove(self):
        # verifier l'existence d'un mouvement à annuler
        if len(self.moveLog) != 0:
            # retire le dernier mouvement et le retourne dans move
            move = self.moveLog.pop()

            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            # change le trait
            self.whiteToMove = not self.whiteToMove
            # mis a jour la position du roi
            if move.pieceMoved == 'wK':
                self.whiteKinglocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKinglocation = (move.startRow, move.startCol)
            # undo castling rights
            self.castleRightsLog.pop()
            self.currentCastlingRight = self.castleRightsLog[-1]
            # undo castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:  # kingside
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else:  # queenside
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'
            # annule un checkmate/staleMate
            self.checkMate = False
            self.staleMate = False

    # *****************************************************************************************************************************************************************************
    # verifie si une case est attaquée par une piece ennemi
    def squareUnderAttack(self, r, c):
        # change le trait
        self.whiteToMove = not self.whiteToMove
        # genere tous les mouvements possibles des pieces ennemis
        oppMoves = self.getAllPossibleMoves()
        # rechange le trait
        self.whiteToMove = not self.whiteToMove
        # verifie si la case (r,c) est attaque par une piece ennemi
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    # *****************************************************************************************************************************************************************************
    # genere tous les mouvements possibles sans verifer si le roi sera en echec
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                # la couleur de la pièce (w=blanc / b=noir)
                turn = self.board[r][c][0]
                # verifier qui a le trait
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    # appelle la fonction qui génère les mouvements valides de la piece concernée (à partir du dictionnaire de fonctions moveFunction)
                    self.moveFunction[piece](r, c, moves)

        return moves

    # *****************************************************************************************************************************************************************************
    # mise a jour les droits de roque
    def updateCastleRights(self, move):
        """ annule la possibilité de faire un roque si le roi ou la tour ont fait un mouvement """
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False  # king side
            self.currentCastlingRight.wqs = False  # queen side
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False  # king side
            self.currentCastlingRight.bqs = False  # queen side
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:  # left rook
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:  # right rook
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:  # left rook
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:  # right rook
                    self.currentCastlingRight.bks = False

        # mise-à-jour des droits si la tour a été capturée
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:  # la tour blanche
                if move.endCol == 0:  # la tour gauche
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:  # la tour droite
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:  # la tour blanche
                if move.endCol == 0:  # la tour gauche
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:  # la tour droite
                    self.currentCastlingRight.bks = False

    # *****************************************************************************************************************************************************************************
    # verifie si une pièce est un pin (bloque une attaque contre le roi), et la direction de cette attaque
    def get_Piece_Pinned(self, row, col):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        return piecePinned, pinDirection

    # *****************************************************************************************************************************************************************************
    # génère les mouvements du pion
    def get_Pawn_moves(self, row, col, moves):
        piecePinned, pinDirection = self.get_Piece_Pinned(row, col)
        moves += Pawn(self.board[row][col][0], row, col).get_available_moves(self.board, piecePinned, pinDirection)
        return moves

    # *****************************************************************************************************************************************************************************
    # génère les mouvements du cavalier
    def get_Knight_moves(self, row, col, moves):
        piecePinned, pinDirection = self.get_Piece_Pinned(row, col)
        moves += Knight(self.board[row][col][0], row, col).get_available_moves(self.board, piecePinned)
        return moves

    # *****************************************************************************************************************************************************************************
    # génère les mouvements de la tour
    def get_Rook_moves(self, row, col, moves):
        piecePinned, pinDirection = self.get_Piece_Pinned(row, col)
        moves += Rook(self.board[row][col][0], row, col).get_available_moves(self.board, piecePinned, pinDirection)
        return moves

    # *****************************************************************************************************************************************************************************
    # génère les mouvements du fou
    def get_Bishop_moves(self, row, col, moves):
        piecePinned, pinDirection = self.get_Piece_Pinned(row, col)
        moves += Bishop(self.board[row][col][0], row, col).get_available_moves(self.board, piecePinned, pinDirection)
        return moves

    # *****************************************************************************************************************************************************************************
    # génère les mouvements de la dame
    def get_Queen_moves(self, row, col, moves):
        piecePinned, pinDirection = self.get_Piece_Pinned(row, col)
        moves += Queen(self.board[row][col][0], row, col).get_available_moves(self.board, piecePinned, pinDirection)
        return moves

    # *****************************************************************************************************************************************************************************
    # la classe king est un special donc on la définit ici
    def get_King_moves(self, row, col, moves):
        moves += King(self.board[row][col][0], row, col).get_available_moves(self)
        return moves

    # *****************************************************************************************************************************************************************************

    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return  # intredit le roque si le roi est en echec
        if (self.whiteToMove and self.currentCastlingRight.wks) or (
                not self.whiteToMove and self.currentCastlingRight.bks):
            self.getkingsideCastleMoves(r, c, moves)  # autorise le roque si les droits sont verifiées

        if (self.whiteToMove and self.currentCastlingRight.wqs) or (
                not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)  # autorise le roque si les droits sont verifiées

    # *****************************************************************************************************************************************************************************
    # genere le mouvement du roque
    def getkingsideCastleMoves(self, r, c, moves):
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--':
            if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2):
                moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove=True))

    # *****************************************************************************************************************************************************************************
    # genere le mouvement du roque
    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == "--":
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))

    # *****************************************************************************************************************************************************************************
    # genere tous les mouvements valides en prenant en compte si le roi est en echec
    def getValidMoves(self):
        moves = []
        # verifie si le roi est en echec, l'existence des pins et des pieces qui attaquent le roi
        self.inCheck, self.checks, self.pins = self.checkForPinsAndChecks()
        # prend les positions des rois
        if self.whiteToMove:
            kingRow = self.whiteKinglocation[0]
            kingCol = self.whiteKinglocation[1]
        else:
            kingRow = self.blackKinglocation[0]
            kingCol = self.blackKinglocation[1]
        if self.inCheck:
            if len(self.checks) == 1:  # une seule piece qui met le roi en echec
                moves = self.getAllPossibleMoves()
                # pour bloquer un echec une piece doit etre mise entre le roi la piece enemie
                check = self.checks[0]  # info de la piece attaquante
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []  # les carrés auxquels les pieces peuvent se déplacer
                # si c'est un cavalier, on doit soit déplacer le roi ou bien capturer le cavalier
                if pieceChecking[1] == "N":
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i,
                                       kingCol + check[3] * i)  # check[2] et check[3] sont les directions d'échec
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[
                            1] == checkCol:  # on sort quand on arrive a la pièce attaquante
                            break
                # pour supprimer les mouvements qui ne bloquent pas l echec ou deplace le roi
                for i in range(len(moves) - 1, -1, -1):  # commencer du debut peut laisser des elements dupliqués
                    if moves[i].pieceMoved[1] != "K":  # movement qui ne déplace pas le roi
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:  # s'il s'agit d'un double échec (2 pieces attaque le roi au meme temps) le roi doit se déplacer
                self.get_King_moves(kingRow, kingCol, moves)
        else:  # s'il n'y pas d'échec
            moves = self.getAllPossibleMoves()

        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col] != "--":
                    self.pieces_left.append(self.board[row][col])
        if "wQ" not in self.board and "bQ" not in self.board:
            self.endGame = True
        if len(moves) == 0:
            if self.inCheck:
                self.checkMate = True
            else:
                self.staleMate = True
        elif len(self.pieces_left) == 2:
            self.staleMate = True
        else:
            self.staleMate = False
            self.staleMate = False
        # self.currentCastlingRight = tempCastleRights
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKinglocation[0], self.whiteKinglocation[1], moves)
        else:
            self.getCastleMoves(self.blackKinglocation[0], self.blackKinglocation[1], moves)
        self.pieces_left = []
        return moves

    # *****************************************************************************************************************************************************************************
    def checkForPinsAndChecks(self):

        pins = []  # piece qui protege le roi contre un échec
        checks = []  # piece enemies qui mettent le roi en échec
        inCheck = False

        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKinglocation[0]  # positions initiales du roiBlanc
            startCol = self.whiteKinglocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKinglocation[0]  # positions initiales du roiNoir
            startCol = self.blackKinglocation[1]

        # cherche les pins et checks à partir de la position du roi
        # les directions à partir du roi :
        # [
        # [(-1,-1),(-1,0),(-1,1)]
        # ,[(0,-1),King,(0,1)]
        # ,[(1,-1),(1,0),(1,1)]
        # ]
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))  # direction des
        # mouvements du roi

        for j in range(len(directions)):
            d = directions[j]
            possiblePins = ()  # reinitialise les pins possibles
            # on vérifie toutes les directions à partir de la position du roi
            for i in range(1,
                           8):  # i représente la distance entre la case du roi et la case de la pièce attaquante/amie
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:  # verifie si la case est à l'intérieur de l'échiquier
                    # si on rencontre une piece
                    endPiece = self.board[endRow][endCol]
                    # on vérifie si elle est amie ou enemie
                    # si elle est ami, elle a la possibilité de devenir un pin
                    if endPiece[0] == allyColor and endPiece[1] != "K":  # verifier si c'est un ami ou ennemie, on a
                        # ajouté endPiece[1] != "K" pour éviter
                        # que le roi voit lui meme comme pin
                        if possiblePins == ():  # la premiere piece amie rencontrée est bloquée
                            # on ajoute la pièce qui peut-être pin
                            possiblePins = (endRow, endCol, d[0], d[1])
                        # cas où deux pièces/ou plusieurs existent entre le roi et la pièce attaquante
                        else:  # 2ᵉ piece n'est pas bloquée
                            break
                    elif endPiece[0] == enemyColor:
                        pieceType = endPiece[1]
                        """ici on a plusieurs cas possible 
                            si la piece est otho au roi et c'est une Tour
                            si la piece attaque diagonalement et c'est un fou
                            si la piece est à un carré du roi diagonalement et c'est un pion
                            si la piece est une reine, on considère tous les directions
                            si la piece est un roi, on considère tous les directions à un carré du roi
                            (interdire au roi de se déplacer à une case contrôlée par un roi enemie)
                        """
                        # j de 0 à 3 sont les directions othos, j de 4 à 7 sont les directions diagos
                        if (0 <= j <= 3 and pieceType == "R") or \
                                (4 <= j <= 7 and pieceType == "B") or \
                                (i == 1 and pieceType == "P" and (
                                        (enemyColor == "w" and 6 <= j <= 7) or (enemyColor == "b" and 4 <= j <= 5))) or \
                                (pieceType == "Q") or (i == 1 and pieceType == "K"):
                            if possiblePins == ():  # ya pas de piece qui bloque , donc echec
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:  # piece qui bloque donc c'est un pin
                                pins.append(possiblePins)
                                break
                        else:  # si la piece ennemie ne met pas le roi en échec
                            break

        # le cavalier est spécial puisqu'on ne peut pas bloquer son attaque avec une pièce
        # on peut soit le capturer, soit déplacer le roi
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == "N":  # cavalier enemies attaquant le roi
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, checks, pins

# *****************************************************************************************************************************************************************************

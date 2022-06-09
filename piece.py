from Move import *


class Piece:
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.available_moves = []

    def clear_available_moves(self):
        self.available_moves = []


# *****************************************************************************************************************************************************************************
class Pawn(Piece):
    def get_available_moves(self, Board, piecePinned, pinDirection):
        self.clear_available_moves()
        row = self.row
        col = self.col
        if self.color == "w":
            if row - 1 >= 0:
                if Board[row - 1][col] == "--":
                    if not piecePinned or pinDirection == (-1, 0):
                        self.available_moves.append(Move((row, col), (row - 1, col), Board))
                        if row == 6:
                            if Board[row - 2][col] == "--":
                                self.available_moves.append(Move((row, col), (row - 2, col), Board))
                if col - 1 >= 0:
                    if Board[row - 1][col - 1] != "--":
                        piece = Board[row - 1][col - 1]
                        if piece[0] != self.color:
                            if not piecePinned or pinDirection == (-1, -1):
                                self.available_moves.append(Move((row, col), (row - 1, col - 1), Board))

                if col + 1 < len(Board[0]):
                    if Board[row - 1][col + 1] != "--":
                        piece = Board[row - 1][col + 1]
                        if piece[0] != self.color:
                            if not piecePinned or pinDirection == (-1, 1):
                                self.available_moves.append(Move((row, col), (row - 1, col + 1), Board))

        if self.color == "b":
            if row + 1 < len(Board):
                if Board[row + 1][col] == "--":
                    if not piecePinned or pinDirection == (1, 0):
                        self.available_moves.append(Move((row, col), (row + 1, col), Board))
                        if row == 1:
                            if Board[row + 2][col] == "--":
                                self.available_moves.append(Move((row, col), (row + 2, col), Board))

                if col - 1 >= 0:
                    if Board[row + 1][col - 1] != "--":
                        piece = Board[row + 1][col - 1]
                        if piece[0] != self.color:
                            if not piecePinned or pinDirection == (1, -1):
                                self.available_moves.append(Move((row, col), (row + 1, col - 1), Board))

                if col + 1 < len(Board):
                    if Board[row + 1][col + 1] != "--":
                        piece = Board[row + 1][col + 1]
                        if piece[0] != self.color:
                            if not piecePinned or pinDirection == (1, 1):
                                self.available_moves.append(Move((row, col), (row + 1, col + 1), Board))

        return self.available_moves


# *****************************************************************************************************************************************************************************
class Knight(Piece):

    def get_available_moves(self, Board, piecePinned):
        self.clear_available_moves()
        row = self.row
        col = self.col
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = row + m[0]
            endCol = col + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = Board[endRow][endCol]
                    if endPiece[0] != self.color:
                        self.available_moves.append(Move((row, col), (endRow, endCol), Board))
        return self.available_moves


# *****************************************************************************************************************************************************************************
class Bishop(Piece):

    def get_available_moves(self, Board, piecePinned, pinDirection):
        self.clear_available_moves()
        row = self.row
        col = self.col
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))

        if self.color == "w":
            enemyColor = "b"
        else:
            enemyColor = "w"
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = Board[endRow][endCol]
                        if endPiece == "--":
                            self.available_moves.append(Move((row, col), (endRow, endCol), Board))
                        elif endPiece[0] == enemyColor:
                            self.available_moves.append(Move((row, col), (endRow, endCol), Board))
                            break
                        else:
                            break
                else:
                    break
        return self.available_moves


# *****************************************************************************************************************************************************************************
class Rook(Piece):

    def get_available_moves(self, Board, piecePinned, pinDirection):
        self.clear_available_moves()

        row = self.row
        col = self.col
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        if self.color == "w":
            enemyColor = "b"
        else:
            enemyColor = "w"
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = Board[endRow][endCol]
                        if endPiece == "--":
                            self.available_moves.append(Move((row, col), (endRow, endCol), Board))
                        elif endPiece[0] == enemyColor:
                            self.available_moves.append(Move((row, col), (endRow, endCol), Board))
                            break
                        else:
                            break
                else:
                    break
        return self.available_moves


# *****************************************************************************************************************************************************************************
class Queen(Piece):
    def get_available_moves(self, Board, piecePinned, pinDirection):
        self.clear_available_moves()

        row = self.row
        col = self.col

        # rook movements
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        if self.color == "w":
            enemyColor = "b"
        else:
            enemyColor = "w"
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = Board[endRow][endCol]
                        if endPiece == "--":
                            self.available_moves.append(Move((row, col), (endRow, endCol), Board))
                        elif endPiece[0] == enemyColor:
                            self.available_moves.append(Move((row, col), (endRow, endCol), Board))
                            break
                        else:
                            break
                else:
                    break

        # bishop movements
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = Board[endRow][endCol]
                        if endPiece == "--":
                            self.available_moves.append(Move((row, col), (endRow, endCol), Board))
                        elif endPiece[0] == enemyColor:
                            self.available_moves.append(Move((row, col), (endRow, endCol), Board))
                            break
                        else:
                            break
                else:
                    break
        return self.available_moves


# *****************************************************************************************************************************************************************************
class King(Piece):
    def get_available_moves(self, gs):
        self.clear_available_moves()
        if gs.whiteToMove:
            allyColor = "w"
        else:
            allyColor = "b"

        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)

        row = self.row
        col = self.col
        for i in range(len(gs.board)):
            endRow = row + rowMoves[i]
            endCol = col + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = gs.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    if allyColor == "w":
                        gs.whiteKinglocation = (endRow, endCol)
                    else:
                        gs.blackKinglocation = (endRow, endCol)
                    inCheck, checks, pins = gs.checkForPinsAndChecks()
                    if not inCheck:
                        self.available_moves.append(Move((row, col), (endRow, endCol), gs.board))

                    if allyColor == "w":
                        gs.whiteKinglocation = (row, col)
                    else:
                        gs.blackKinglocation = (row, col)
        return self.available_moves

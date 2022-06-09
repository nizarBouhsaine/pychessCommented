# classe pour recevoir les inputs des mouvements

class Move:
    "dictionnnaire pour traduire les postions sur ecrans en notations d'échec "
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board,isCastleMove=False):
        # startsq fait reference à la case de la piece qui va bouger
        self.startSq = startSq
        self.endSq = endSq
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        # endsq fait reference à la case ou la piece va bouger
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        # pieceMoved stocke la piece qui va bouger
        self.pieceMoved = board[self.startRow][self.startCol]
        # pieceCaptured stocke la piece qui va être capturer
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isCastleMove = isCastleMove
        # variable pour verifier s'il s'agit d'une promotion du pion
        self.isPawnPromotion = False
        self.isPawnPromotion = (self.pieceMoved == "wP" and self.endRow == 0) or (self.pieceMoved == "bP" and self.endRow == 7)

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    # deux fonctions pour traduire les mouvements sur ecrans en notations d'echec

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID

    # affiche les icones des pieces+l'emplacement de la case de début et de fin
    def getChessNotation(self):
        pieceToUnicode = {
            "bK": "\U00002654", "bQ": "\U00002655", "bN": "\U00002658", "bB": "\U00002657", "bP": "\U00002659",
            "bR": "\U00002656",
            "wK": "\U0000265A", "wQ": "\U0000265B", "wN": "\U0000265E", "wB": "\U0000265D", "wP": "\U0000265F",
            "wR": "\U0000265C",
        }
        icon = pieceToUnicode[self.pieceMoved]
        return icon + self.getRanksFiles(self.startCol, self.startRow) + self.getRanksFiles(self.endCol, self.endRow)

    # transfrome les cols et lignes sur l'ecran en notation d'echec
    def getRanksFiles(self, c, r):
        return self.colsToFiles[c] + self.rowsToRanks[r]

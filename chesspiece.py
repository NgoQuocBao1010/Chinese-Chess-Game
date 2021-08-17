import pygame
from pprint import pprint

from utils import Color, ChessImages, Configuration

RED_SIDE = Configuration.RED_SIDE
BLUE_SIDE = Configuration.BLUE_SIDE


class ChessPiece:
    NOT_SELECTED = 0
    SELECTED = 1

    NAME = "A chess piece"

    def __init__(self, centrePoint=(0, 0), position=(0, 0), side=RED_SIDE):
        self.position = position
        self.centrePoint = centrePoint
        self.radius = 20

        self.side = side
        self.status = self.NOT_SELECTED
        self.possibleMoves = []
        self.blockAttackMoves = []
        self.image = None

    def draw(self, win):
        """
        Draw the piece
        """
        pygame.draw.circle(win, Color.WHITE, self.centrePoint, self.radius)
        x, y = self.centrePoint
        if self.status == self.SELECTED:
            pygame.draw.rect(win, Color.GREEN, pygame.Rect(x - self.radius - 1, y - self.radius - 1, self.radius * 2 + 2, self.radius * 2 + 2), 2)

        if self.image:
            win.blit(self.image, (x - self.radius, y - self.radius))

    def isClicked(self, pos=None):
        """
        Check if the piece is clicked
        """
        if not pos:
            return None

        clickX, clickY = pos
        centerX, centerY = self.centrePoint

        if (clickX - centerX) ** 2 + (clickY - centerY) ** 2 < self.radius ** 2:
            return True
        return False

    def changeStatus(self, selected=False):
        """
        Change the color when ever piece is seleceted
        """
        self.status = self.SELECTED if selected else self.NOT_SELECTED

    def checkPossibleMove(self, boardGrid):
        '''
        Checking all possible moves of the piece
        '''
        print("This is not a real chesspiece")

    def moveToNewSpot(self, centrePoint=None, position=None):
        if not centrePoint:
            return

        self.centrePoint = centrePoint
        self.position = position

    def isEnemy(self, other):
        return True if other.side != self.side else False
    
    def __str__(self):
        return f"A {self.NAME} at {self.position}"
    
    def __repr__(self):
        return f"{self.NAME}-{self.side}"


class Chariot(ChessPiece):
    """
    Chariot chess piece
    """

    NAME = "Chariot"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = ChessImages.RED_CHARIOT if self.side == RED_SIDE else ChessImages.BLUE_CHARIOT

    def checkPossibleMove(self, boardGrid, update=True, forceMoves=None):
        movables = []

        rowPos, colPos = self.position

        column = boardGrid[:, colPos]  # get the whole colummn
        # Move up
        for r in range(
            rowPos - 1, -1, -1
        ):  # get all the row above current row, except current row
            if not column[r]:
                movables.append((r, colPos))
            else:
                otherPiece = column[r]
                if self.isEnemy(otherPiece):
                    movables.append((r, colPos))
                break

        # Move down
        for r in range(rowPos + 1, 10):
            if not column[r]:
                movables.append((r, colPos))
            else:
                otherPiece = column[r]
                if self.isEnemy(otherPiece):
                    movables.append((r, colPos))
                break

        row = boardGrid[rowPos]  # get the whole row
        # Move left
        for c in range(colPos - 1, -1, -1):
            if not row[c]:
                movables.append((rowPos, c))
            else:
                otherPiece = row[c]
                if self.isEnemy(otherPiece):
                    movables.append((rowPos, c))
                break

        # Move right
        for c in range(colPos + 1, 9):
            if not row[c]:
                movables.append((rowPos, c))
            else:
                otherPiece = row[c]
                if self.isEnemy(otherPiece):
                    movables.append((rowPos, c))
                break
        
        if forceMoves:
            movables = [move for move in movables if move in forceMoves]
        
        if update:
            self.possibleMoves = movables

        return movables


class Horse(ChessPiece):
    """
    Horse Chess Piece
    """

    NAME = "Horse"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = ChessImages.RED_HORSE if self.side == RED_SIDE else ChessImages.BLUE_HORSE

    def checkPossibleMove(self, boardGrid, update=True, forceMoves=None):
        movables = []

        rowPos, colPos = self.position

        # All possibles move of a Knight
        moveX = []
        moveY = []

        # Move up
        stepX = [-2, -2]
        stepY = [-1, 1]
        if 0 <= rowPos - 1 and not boardGrid[rowPos - 1, colPos]:
            moveX += stepX
            moveY += stepY

        # Move down
        stepX = [2, 2]
        stepY = [-1, 1]
        if rowPos + 1 <= 9 and not boardGrid[rowPos + 1, colPos]:
            moveX += stepX
            moveY += stepY

        # Move left
        stepX = [1, -1]
        stepY = [-2, -2]
        if 0 <= colPos - 1 and not boardGrid[rowPos, colPos - 1]:
            moveX += stepX
            moveY += stepY

        # Move right
        stepX = [1, -1]
        stepY = [2, 2]
        if colPos + 1 <= 8 and not boardGrid[rowPos, colPos + 1]:
            moveX += stepX
            moveY += stepY

        for mX, mY in zip(moveX, moveY):
            newRow = rowPos + mX
            newCol = colPos + mY
            
            # Check if the move is valid
            if 0 <= newRow <= 9 and 0 <= newCol <= 8:
                if not boardGrid[newRow, newCol]:
                    movables.append((newRow, newCol))
                else:
                    otherPiece = boardGrid[newRow, newCol]
                    if self.isEnemy(otherPiece):
                        movables.append((newRow, newCol))
        
        if forceMoves:
            movables = [move for move in movables if move in forceMoves]

        if update:
            self.possibleMoves = movables

        # print(f"Done cheking move from Horse side {self.side}\n")
        # pprint(boardGrid)
        return movables


class Elephant(ChessPiece):
    """
    Horse Chess Piece
    """

    NAME = "Elephant"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.moveLimit = (0, 4) if 0 <= self.position[0] <= 4 else (5, 9)
        self.image = ChessImages.RED_ELEPHANT if self.side == RED_SIDE else ChessImages.BLUE_ELEPHANT

    def checkPossibleMove(self, boardGrid, update=True, forceMoves=None):
        movables = []

        rowPos, colPos = self.position

        upLimit, downLimt = self.moveLimit

        # Move up left
        if (
            rowPos - 1 >= upLimit
            and colPos - 1 >= 0
            and not boardGrid[rowPos - 1, colPos - 1]
        ):
            if rowPos - 2 >= upLimit and colPos - 2 >= 0:
                if not boardGrid[rowPos - 2, colPos - 2]:
                    movables.append((rowPos - 2, colPos - 2))
                else:
                    otherPiece = boardGrid[rowPos - 2, colPos - 2]
                    if self.isEnemy(otherPiece):
                        movables.append((rowPos - 2, colPos - 2))

        # Move up right
        if (
            rowPos - 1 >= upLimit
            and colPos + 1 <= 8
            and not boardGrid[rowPos - 1, colPos + 1]
        ):
            if rowPos - 2 >= upLimit and colPos + 2 <= 8:
                if not boardGrid[rowPos - 2, colPos + 2]:
                    movables.append((rowPos - 2, colPos + 2))
                else:
                    otherPiece = boardGrid[rowPos - 2, colPos + 2]
                    if self.isEnemy(otherPiece):
                        movables.append((rowPos - 2, colPos + 2))

        # Move down left
        if (
            rowPos + 1 <= downLimt
            and colPos - 1 >= 0
            and not boardGrid[rowPos + 1, colPos - 1]
        ):
            if rowPos + 2 >= upLimit and colPos - 2 >= 0:
                if not boardGrid[rowPos + 2, colPos - 2]:
                    movables.append((rowPos + 2, colPos - 2))
                else:
                    otherPiece = boardGrid[rowPos + 2, colPos - 2]
                    if self.isEnemy(otherPiece):
                        movables.append((rowPos + 2, colPos - 2))

        # Move down right
        if (
            rowPos + 1 <= downLimt
            and colPos + 1 <= 8
            and not boardGrid[rowPos + 1, colPos + 1]
        ):
            if rowPos + 2 >= upLimit and colPos + 2 <= 8:
                if not boardGrid[rowPos + 2, colPos + 2]:
                    movables.append((rowPos + 2, colPos + 2))
                else:
                    otherPiece = boardGrid[rowPos + 2, colPos + 2]
                    if self.isEnemy(otherPiece):
                        movables.append((rowPos + 2, colPos + 2))

        if forceMoves:
            movables = [move for move in movables if move in forceMoves]
        
        if update:
            self.possibleMoves = movables

        return movables


class Lord(ChessPiece):
    NAME = "Lord"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.moveLimit = (0, 2) if 0 <= self.position[0] <= 2 else (7, 9)
        self.image = ChessImages.RED_LORD if self.side == RED_SIDE else ChessImages.BLUE_LORD
        self.mated = False

        # Animation when lord is under attack
        self.grow = True
        self.thickness = 4
        self.skip = True

    
    def draw(self, win):
        super().draw(win)
        if self.mated:
            if self.grow:
                self.thickness += 1
            else:
                self.thickness -= 1

            if self.thickness == 6:
                self.grow = False
            if self.thickness <= 4:
                self.grow = True

            pygame.draw.circle(win, Color.RED, self.centrePoint, self.radius + self.thickness, self.thickness)
    
    def checkPossibleMove(self, boardGrid, update=True, avoidMoves=None):
        movables = []

        rowPos, colPos = self.position

        upLimit, downLimt = self.moveLimit
        leftLimit, rightLimit = (3, 5)

        movesX = [0, 0, 1, -1]
        movesY = [-1, 1, 0, 0]

        for mX, mY in zip(movesX, movesY):
            newRow = rowPos + mX
            newCol = colPos + mY

            # Check if the move is valid
            if upLimit <= newRow <= downLimt and leftLimit <= newCol <= rightLimit:
                if not boardGrid[newRow, newCol]:
                    movables.append((newRow, newCol))
                else:
                    otherPiece = boardGrid[newRow, newCol]
                    if self.isEnemy(otherPiece):
                        movables.append((newRow, newCol))

        if avoidMoves:
            movables = [move for move in movables if move not in avoidMoves]

        if update:
            self.possibleMoves = movables

        return movables

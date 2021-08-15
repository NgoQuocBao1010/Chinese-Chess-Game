import pygame
import numpy as np
from pprint import pprint

from utils import Color, ChessImages


class ChessPiece:
    NOT_SELECTED = 0
    SELECTED = 1

    STATUS_COLOR = {
        0: Color.GREEN,
        1: Color.RED,
    }

    NAME = "A chess piece"
    IMAGE = None

    def __init__(self, centrePoint=(0, 0), position=(0, 0)):
        self.position = position
        self.centrePoint = centrePoint
        self.radius = 15

        self.status = self.NOT_SELECTED
        self.posibleMoves = []

    def draw(self, win):
        """
        Draw the piece
        """
        color = self.STATUS_COLOR.get(self.status)
        pygame.draw.circle(win, Color.WHITE, self.centrePoint, self.radius)
        x, y = self.centrePoint

        if self.IMAGE:
            win.blit(self.IMAGE, (x - self.radius, y - self.radius))

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
        print("This is not a real chesspiece")
        return None

    def moveToNewSpot(self, centrePoint=None, position=None):
        if not centrePoint:
            return

        self.centrePoint = centrePoint
        self.position = position

    def __str__(self):
        return f"A {self.NAME} at {self.position}"


class Chariot(ChessPiece):
    """
    Chariot chess piece
    """

    NAME = "Chariot"
    IMAGE = ChessImages.RED_CHARIOT

    def __init__(self, centrePoint=(0, 0), position=(0, 0)):
        super().__init__(centrePoint, position)

    def checkPossibleMove(self, boardGrid):
        movables = []
        boardGrid = np.array(boardGrid)

        rowPos, colPos = self.position

        column = boardGrid[:, colPos]  # get the whole colummn
        # Move up
        for r in range(
            rowPos - 1, -1, -1
        ):  # get all the row above current row, except current row
            if not column[r]:
                movables.append((r, colPos))
            else:
                break

        # Move down
        for r in range(rowPos + 1, 10):
            if not column[r]:
                movables.append((r, colPos))
            else:
                break

        row = boardGrid[rowPos]  # get the whole row
        # Move left
        for c in range(colPos - 1, -1, -1):
            if not row[c]:
                movables.append((rowPos, c))
            else:
                break
        # Move right
        for c in range(colPos + 1, 9):
            if not row[c]:
                movables.append((rowPos, c))
            else:
                break

        return movables


class Horse(ChessPiece):
    """
    Horse Chess Piece
    """

    NAME = "Horse"
    IMAGE = ChessImages.RED_HORSE

    def __init__(self, centrePoint=(0, 0), position=(0, 0)):
        super().__init__(centrePoint, position)

    def checkPossibleMove(self, boardGrid):
        movables = []
        boardGrid = np.array(boardGrid)

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
            if 0 <= newRow <= 9 and 0 <= newCol <= 8 and not boardGrid[newRow, newCol]:
                movables.append((newRow, newCol))

        return movables


class Elephant(ChessPiece):
    """
    Horse Chess Piece
    """

    NAME = "Elephant"
    IMAGE = ChessImages.RED_ELEPHANT

    def __init__(self, centrePoint=(0, 0), position=(0, 0)):
        super().__init__(centrePoint, position)
        self.moveLimit = (0, 4) if 0 <= self.position[0] <= 4 else (5, 9)

    def checkPossibleMove(self, boardGrid):
        movables = []
        boardGrid = np.array(boardGrid)

        rowPos, colPos = self.position

        upLimit, downLimt = self.moveLimit

        # Move up left
        if (
            rowPos - 1 >= upLimit
            and colPos - 1 >= 0
            and not boardGrid[rowPos - 1, colPos - 1]
        ):
            if rowPos - 2 >= upLimit and colPos - 2 >= 0:
                movables.append((rowPos - 2, colPos - 2))

        # Move up right
        if (
            rowPos - 1 >= upLimit
            and colPos + 1 <= 8
            and not boardGrid[rowPos - 1, colPos + 1]
        ):
            if rowPos - 2 >= upLimit and colPos + 2 <= 8:
                movables.append((rowPos - 2, colPos + 2))

        # Move down left
        if (
            rowPos + 1 <= downLimt
            and colPos - 1 >= 0
            and not boardGrid[rowPos + 1, colPos - 1]
        ):
            if rowPos + 2 >= upLimit and colPos - 2 >= 0:
                movables.append((rowPos + 2, colPos - 2))

        # Move down right
        if (
            rowPos + 1 <= downLimt
            and colPos + 1 <= 8
            and not boardGrid[rowPos + 1, colPos + 1]
        ):
            if rowPos + 2 >= upLimit and colPos + 2 <= 8:
                movables.append((rowPos + 2, colPos + 2))

        return movables

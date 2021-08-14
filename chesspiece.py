import pygame
import numpy as np
from pprint import pprint

from utils import Color


class ChessPiece:
    NOT_SELECTED = 0
    SELECTED = 1

    STATUS_COLOR = {
        0: Color.GREEN,
        1: Color.RED,
    }

    def __init__(self, centrePoint=(0, 0), position=(0, 0)):
        self.position = position
        self.centrePoint = centrePoint
        self.radius = 10

        self.status = self.NOT_SELECTED
        self.posibleMoves = []

    def draw(self, win):
        """
        Draw the piece
        """
        color = self.STATUS_COLOR.get(self.status)
        pygame.draw.circle(win, color, self.centrePoint, self.radius)

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


class Rook(ChessPiece):
    def __init__(self, centrePoint=(0, 0), position=(0, 0)):
        super().__init__(centrePoint, position)

    def isClicked(self, pos=None):
        return super().isClicked(pos)

    def checkPossibleMove(self, boardGrid):
        movables = []
        boardGrid = np.array(boardGrid)

        rowPos, colPos = self.position

        row = boardGrid[rowPos]
        for col, occupied in enumerate(row):
            if not occupied:
                movables.append((rowPos, col))

        col = boardGrid[:, colPos]
        for row, occupied in enumerate(col):
            if not occupied:
                movables.append((row, colPos))

        print(movables)
        return movables
